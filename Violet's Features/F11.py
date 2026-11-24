"""Searches hundreds of websites for a username and reports where a public
profile with that name exists. Uses the site list from the open-source
Sherlock project (MIT licensed, bundled as sherlock_sites.json). Enter a
username; a full run checks ~480 sites and can take a minute or two.
Treat hits as leads: a few sites answer 'found' for names that do not exist.
"""
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sherlock_sites.json")
UA = {"User-Agent": "Mozilla/5.0 (VioletTools username search)"}


def _load():
    with open(DATA, encoding="utf-8") as handle:
        raw = json.load(handle)
    sites = {}
    for name, info in raw.items():
        if name.startswith("$") or not isinstance(info, dict):
            continue
        if "url" in info and "errorType" in info:
            sites[name] = info
    return sites


def _is_found(info, status, text):
    kind = info["errorType"]
    if kind == "message":
        msgs = info.get("errorMsg", "")
        if isinstance(msgs, str):
            msgs = [msgs]
        return not any(m in text for m in msgs)
    if kind == "status_code":
        codes = info.get("errorCode")
        if codes is not None:
            codes = [codes] if isinstance(codes, int) else codes
            if status in codes:
                return False
        return 200 <= status < 300
    if kind == "response_url":
        return 200 <= status < 300
    return False


def _check(item, username):
    name, info = item
    regex = info.get("regexCheck")
    if regex and not re.search(regex, username):
        return name, None, None
    encoded = urllib.parse.quote(username)
    try:
        url = info["url"].format(encoded)
        probe = info.get("urlProbe")
        target = probe.format(encoded) if probe else url
    except Exception:
        return name, None, None
    headers = dict(UA)
    headers.update(info.get("headers", {}))
    method = info.get("request_method", "GET")
    data = None
    if method == "POST" and "request_payload" in info:
        try:
            payload = json.loads(json.dumps(info["request_payload"]).replace("{}", username))
            data = urllib.parse.urlencode(payload).encode()
        except Exception:
            data = None
    need_body = info["errorType"] == "message"
    request = urllib.request.Request(target, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            status = response.status
            text = response.read(30000).decode("utf-8", "replace") if need_body else ""
    except urllib.error.HTTPError as error:
        status = error.code
        text = error.read(30000).decode("utf-8", "replace") if need_body else ""
    except Exception:
        return name, "error", url
    return name, ("found" if _is_found(info, status, text) else "none"), url


def F11():
    print("\033[0;95m== Username Search ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    username = input("Username: ").strip()
    if not username:
        print("No username given.")
        return
    try:
        sites = _load()
    except Exception as error:
        print("Could not load the site list:", error)
        return
    nsfw = input("Include adult (NSFW) sites? [y/N]: ").strip().lower().startswith("y")
    items = [(n, i) for n, i in sites.items() if nsfw or not i.get("isNSFW")]
    total = len(items)
    print(f"\nSearching {total} sites for '{username}' ... this can take a minute.\n")
    found = []
    errors = 0
    with ThreadPoolExecutor(max_workers=30) as pool:
        futures = {pool.submit(_check, item, username): item[0] for item in items}
        for future in as_completed(futures):
            name, status, url = future.result()
            if status == "found":
                found.append((name, url))
                print(f"  \033[0;92m[+]\033[0m {name}: {url}")
            elif status == "error":
                errors += 1
    print(f"\n\033[0;97mFound {len(found)} profiles across {total} sites "
          f"({errors} errors/timeouts).\033[0m")
