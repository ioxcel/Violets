"""Looks up a public Discord invite (a discord.gg link or just the code)
and shows what it points to: server name, ID, description, approximate
member and online counts, verification level, server features, the
channel it lands in, and who created it. It only reads Discord's public
invite data and does NOT join the server. Expired or invalid codes
return nothing.
"""
import json
import re
import urllib.error
import urllib.request

VERIFICATION = {0: "None", 1: "Low", 2: "Medium", 3: "High", 4: "Very High"}
CHANNEL_TYPES = {
    0: "text", 2: "voice", 4: "category", 5: "announcement",
    13: "stage", 15: "forum",
}


def F22():
    print("\033[0;95m== Invite Inspector ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    raw = input("Invite (link or code): ").strip()
    match = re.search(r"(?:discord\.(?:gg|com/invite)/)?([A-Za-z0-9-]+)/?$", raw)
    code = match.group(1) if match else ""
    if not code:
        print("Enter a valid invite code or link.")
        return
    url = f"https://discord.com/api/v10/invites/{code}?with_counts=true&with_expiration=true"
    request = urllib.request.Request(url, headers={"User-Agent": "VioletTools/1.0"})
    print("Looking up invite ...")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            print("Invite is invalid or expired.")
        else:
            print("Lookup failed:", error)
        return
    except Exception as error:
        print("Lookup failed:", error)
        return
    guild = data.get("guild") or {}
    channel = data.get("channel") or {}
    inviter = data.get("inviter") or {}
    print(f"\n\033[0;97mServer:\033[0m        {guild.get('name', '-')}")
    print(f"\033[0;97mServer ID:\033[0m     {guild.get('id', '-')}")
    if guild.get("description"):
        print(f"\033[0;97mDescription:\033[0m   {guild['description']}")
    print(f"\033[0;97mMembers:\033[0m       ~{data.get('approximate_member_count', '?')}")
    print(f"\033[0;97mOnline:\033[0m        ~{data.get('approximate_presence_count', '?')}")
    print(f"\033[0;97mVerification:\033[0m  {VERIFICATION.get(guild.get('verification_level'), '?')}")
    boosts = guild.get("premium_subscription_count")
    if boosts is not None:
        print(f"\033[0;97mBoosts:\033[0m        {boosts}")
    channel_type = CHANNEL_TYPES.get(channel.get("type"), channel.get("type"))
    print(f"\033[0;97mChannel:\033[0m       #{channel.get('name', '-')} ({channel_type})")
    if inviter:
        tag = inviter.get("username", "")
        if inviter.get("discriminator") and inviter["discriminator"] != "0":
            tag += "#" + inviter["discriminator"]
        print(f"\033[0;97mInviter:\033[0m       {tag} ({inviter.get('id', '-')})")
    if data.get("expires_at"):
        print(f"\033[0;97mExpires:\033[0m       {data['expires_at']}")
    features = guild.get("features") or []
    if features:
        print(f"\033[0;97mFeatures:\033[0m      {', '.join(sorted(features))}")
