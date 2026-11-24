"""Sends test messages to one of YOUR OWN Discord webhooks, so you can
check an integration works and see how it handles volume. You choose
whether each message is a plain message or a rich embed, the text, the
sender name it shows as, an optional avatar, and how many copies to send
(1-100). It confirms first, then sends them one at a time while respecting
Discord's rate limits -- if Discord asks it to slow down it waits, so this
is a throughput test, not a flood tool. After a run it can repeat with the
same details or fresh ones. Only use it on webhooks you own; do not post
into servers or channels you are not allowed to. A webhook URL is a secret;
keep it private.
"""
import json
import re
import time
import urllib.error
import urllib.request

WEBHOOK = re.compile(r"discord(?:app)?\.com/api/(?:v\d+/)?webhooks/(\d+)/([\w-]+)")
SEND_DELAY = 0.4
MAX_RETRIES = 5


def _color(text):
    text = text.strip().lstrip("#")
    if not text:
        return None
    try:
        return int(text, 16)
    except ValueError:
        return None


def _collect():
    raw = input("Webhook URL: ").strip()
    match = WEBHOOK.search(raw)
    if not match:
        print("That does not look like a Discord webhook URL.")
        return None
    mode = input("Send as [e]mbed or [n]ormal message? [n]: ").strip().lower()
    mode = "embed" if mode in ("e", "embed") else "normal"
    content = input("Message: ").strip()
    if not content:
        print("Nothing to send.")
        return None
    title = color = None
    if mode == "embed":
        title = input("Embed title (optional): ").strip() or None
        color = _color(input("Embed colour hex, e.g. FF55FF (optional): "))
    username = input("From / sender name (optional): ").strip()
    avatar = input("Override avatar URL (optional): ").strip()
    details = {
        "api": f"https://discord.com/api/v10/webhooks/{match.group(1)}/{match.group(2)}?wait=true",
        "mode": mode, "content": content, "title": title, "color": color,
        "username": username, "avatar": avatar,
    }
    return details


def _body(details):
    if details["mode"] == "embed":
        embed = {"description": details["content"]}
        if details["title"]:
            embed["title"] = details["title"]
        if details["color"] is not None:
            embed["color"] = details["color"]
        payload = {"embeds": [embed]}
    else:
        payload = {"content": details["content"]}
    if details["username"]:
        payload["username"] = details["username"]
    if details["avatar"]:
        payload["avatar_url"] = details["avatar"]
    return json.dumps(payload).encode()


def _send(api, body):
    for _ in range(MAX_RETRIES):
        request = urllib.request.Request(
            api, data=body,
            headers={"User-Agent": "VioletTools/1.0", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return True, json.load(response).get("id", "-")
        except urllib.error.HTTPError as error:
            if error.code == 429:
                try:
                    wait = float(json.load(error).get("retry_after", 1))
                except Exception:
                    wait = float(error.headers.get("Retry-After", 1) or 1)
                print(f"  rate limited, waiting {wait:.1f}s ...")
                time.sleep(wait + 0.1)
                continue
            return False, f"{error.code}: {error.read().decode(errors='replace')}"
        except Exception as error:
            return False, str(error)
    return False, "gave up after repeated rate limits"


def _run_batch(details):
    amount = input("How many copies? [1-100, default 1]: ").strip() or "1"
    if not amount.isdigit() or not 1 <= int(amount) <= 100:
        print("Enter a whole number from 1 to 100.")
        return
    amount = int(amount)
    kind = "embed" if details["mode"] == "embed" else "message"
    noun = kind if amount == 1 else kind + "s"
    if input(f"\nSend {amount} {noun} now? [y/N]: ").strip().lower() not in ("y", "yes"):
        print("Cancelled.")
        return
    body = _body(details)
    sent = 0
    for index in range(1, amount + 1):
        ok, info = _send(details["api"], body)
        if ok:
            sent += 1
            print(f"  [{index}/{amount}] sent (id {info})")
        else:
            print(f"  [{index}/{amount}] failed: {info}")
            break
        if index < amount:
            time.sleep(SEND_DELAY)
    print(f"\n\033[0;97mDone.\033[0m {sent}/{amount} delivered.")


def F24():
    print("\033[0;95m== Webhook Tester ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    details = _collect()
    if details is None:
        return
    while True:
        _run_batch(details)
        if input("\nRepeat the webhook test? [y/N]: ").strip().lower() not in ("y", "yes"):
            return
        if input("Same details? [y/N]: ").strip().lower() in ("y", "yes"):
            print()
            continue
        print()
        details = _collect()
        if details is None:
            return
