"""Reads the details of one of YOUR OWN Discord webhooks. Paste the full
webhook URL and it shows the webhook's name, ID, the channel and server
it posts to, and its avatar, so you can confirm exactly where a webhook
fires before you use it. This is a read-only lookup: no message is sent.
Only use it on webhook URLs you own; a webhook URL is a secret, so keep
it private.
"""
import json
import re
import urllib.error
import urllib.request

WEBHOOK = re.compile(r"discord(?:app)?\.com/api/(?:v\d+/)?webhooks/(\d+)/([\w-]+)")


def F23():
    print("\033[0;95m== Webhook Inspector ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    raw = input("Webhook URL: ").strip()
    match = WEBHOOK.search(raw)
    if not match:
        print("That does not look like a Discord webhook URL.")
        return
    api = f"https://discord.com/api/v10/webhooks/{match.group(1)}/{match.group(2)}"
    request = urllib.request.Request(api, headers={"User-Agent": "VioletTools/1.0"})
    print("Reading webhook ...")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        if error.code in (401, 404):
            print("Webhook not found (wrong, deleted or revoked URL).")
        else:
            print("Lookup failed:", error)
        return
    except Exception as error:
        print("Lookup failed:", error)
        return
    print(f"\n\033[0;97mName:\033[0m        {data.get('name', '-')}")
    print(f"\033[0;97mWebhook ID:\033[0m  {data.get('id', '-')}")
    print(f"\033[0;97mChannel ID:\033[0m  {data.get('channel_id', '-')}")
    print(f"\033[0;97mServer ID:\033[0m   {data.get('guild_id', '-')}")
    avatar = data.get("avatar")
    if avatar:
        print(f"\033[0;97mAvatar:\033[0m      https://cdn.discordapp.com/avatars/{data['id']}/{avatar}.png")
    else:
        print("\033[0;97mAvatar:\033[0m      (default)")
