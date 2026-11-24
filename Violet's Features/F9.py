"""Checks the Internet Archive's Wayback Machine for saved snapshots of a
URL: whether it is archived, the most recent capture, the earliest capture,
and roughly how many snapshots exist. Great for seeing what a page used to
look like or recovering deleted content. Enter a URL or domain.
"""
import json
import urllib.error
import urllib.parse
import urllib.request


def _get(url):
    request = urllib.request.Request(url, headers={"User-Agent": "VioletTools/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def _stamp(value):
    if not value or len(value) < 14:
        return value or "-"
    return f"{value[0:4]}-{value[4:6]}-{value[6:8]} {value[8:10]}:{value[10:12]}:{value[12:14]}"


def F9():
    print("\033[0;95m== Wayback Machine ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    target = input("URL or domain: ").strip()
    if not target:
        print("Enter a URL.")
        return
    api = "https://archive.org/wayback/available?" + urllib.parse.urlencode({"url": target})
    try:
        data = _get(api)
    except Exception as error:
        print("Wayback lookup failed:", error)
        return
    snapshot = (data.get("archived_snapshots") or {}).get("closest")
    if not snapshot or not snapshot.get("available"):
        print("No snapshots found for that URL.")
        return
    print(f"\n\033[0;97mLatest snapshot:\033[0m  {_stamp(snapshot.get('timestamp'))}")
    print(f"\033[0;97mLink:\033[0m            {snapshot.get('url')}")
    cdx = ("https://web.archive.org/cdx/search/cdx?" + urllib.parse.urlencode(
        {"url": target, "output": "json", "limit": "1", "fl": "timestamp,original"}))
    try:
        rows = _get(cdx)
        if len(rows) > 1:
            first = rows[1]
            print(f"\033[0;97mEarliest:\033[0m        {_stamp(first[0])}")
            print(f"\033[0;97mFirst capture:\033[0m   https://web.archive.org/web/{first[0]}/{first[1]}")
    except Exception:
        pass
    print(f"\n\033[0;90mBrowse all: https://web.archive.org/web/*/{target}\033[0m")
