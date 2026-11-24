"""Builds a Discord rich embed step by step -- title, description, link,
colour, author, footer, images and any number of name/value fields -- and
shows a live preview of the embed card on the right as you fill it in. It
prints the finished embed as JSON you can paste into your own code or bot,
and can optionally post it straight to one of YOUR OWN webhooks to see it
for real. It only sends when you confirm, and only to a webhook URL you
provide.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

WEBHOOK = re.compile(r"discord(?:app)?\.com/api/(?:v\d+/)?webhooks/(\d+)/([\w-]+)")
TRUECOLOR = sys.platform == "win32" or os.environ.get("COLORTERM") in ("truecolor", "24bit")
PREVIEW_COL = 44
WRAP = 40


def _color(text):
    text = text.strip().lstrip("#")
    if not text:
        return None
    try:
        return int(text, 16)
    except ValueError:
        return None


def _bar(color):
    if color is not None and TRUECOLOR:
        return f"\033[38;2;{(color >> 16) & 255};{(color >> 8) & 255};{color & 255}m▌\033[0m"
    return "\033[0;95m▌\033[0m"


def _wrap(text, width):
    lines = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        current = ""
        for word in para.split(" "):
            while len(word) > width:
                if current:
                    lines.append(current)
                    current = ""
                lines.append(word[:width])
                word = word[width:]
            if not current:
                current = word
            elif len(current) + 1 + len(word) <= width:
                current += " " + word
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def _preview(embed):
    bar = _bar(embed.get("color"))
    styled = []

    def add(style, text):
        for line in _wrap(text, WRAP) or [""]:
            styled.append(f"{bar} {style}{line}\033[0m")

    author = (embed.get("author") or {}).get("name")
    if author:
        add("\033[0;90m", author)
    if embed.get("title"):
        add("\033[1;97m", embed["title"])
    if embed.get("description"):
        add("\033[0;37m", embed["description"])
    for field in embed.get("fields", []):
        styled.append(f"{bar}")
        add("\033[0;97m", field["name"])
        add("\033[0;37m", field.get("value", ""))
    if embed.get("image"):
        add("\033[0;90m", "[image] " + embed["image"]["url"])
    if embed.get("thumbnail"):
        add("\033[0;90m", "[thumb] " + embed["thumbnail"]["url"])
    footer = (embed.get("footer") or {}).get("text")
    if footer:
        styled.append(f"{bar}")
        add("\033[0;90m", footer)
    if not styled:
        styled = [f"{bar} \033[0;90m(empty)\033[0m"]
    return ["\033[0;90mPreview\033[0m", ""] + styled


def _render(embed, entries):
    left = [f"\033[0;97m{label}:\033[0m {value or '-'}"[:PREVIEW_COL + 8] for label, value in entries]
    right = _preview(embed)
    out = ["\033[2J\033[H", "\033[0;95m== Embed Builder ==\033[0m   \033[0;90mlive preview →\033[0m", ""]
    for index in range(max(len(left), len(right))):
        l = left[index] if index < len(left) else ""
        r = right[index] if index < len(right) else ""
        pad = PREVIEW_COL - 3 - len(re.sub(r"\033\[[\d;]*m", "", l))
        out.append("   " + l + " " * max(0, pad) + r)
    out.append("")
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()


def _send(embed):
    hook = input("\nPost to a webhook now? Paste URL or leave blank: ").strip()
    if not hook:
        return
    match = WEBHOOK.search(hook)
    if not match:
        print("That does not look like a Discord webhook URL.")
        return
    api = f"https://discord.com/api/v10/webhooks/{match.group(1)}/{match.group(2)}?wait=true"
    request = urllib.request.Request(
        api, data=json.dumps({"embeds": [embed]}).encode(),
        headers={"User-Agent": "VioletTools/1.0", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        print(f"Send failed ({error.code}): {error.read().decode(errors='replace')}")
        return
    except Exception as error:
        print("Send failed:", error)
        return
    print(f"\n\033[0;97mPosted.\033[0m Message ID: {data.get('id', '-')}")


def F25():
    embed = {}
    entries = []

    def ask(label, prompt):
        _render(embed, entries)
        value = input(f"   {prompt}").strip()
        entries.append((label, value))
        return value

    title = ask("Title", "Title (optional): ")
    if title:
        embed["title"] = title
    description = ask("Description", "Description (optional): ")
    if description:
        embed["description"] = description
    url = ask("Link", "Title link URL (optional): ")
    if url:
        embed["url"] = url
    raw_color = ask("Colour", "Colour hex, e.g. FF55FF (optional): ")
    color = _color(raw_color)
    if color is not None:
        embed["color"] = color
    author = ask("Author", "Author name (optional): ")
    if author:
        embed["author"] = {"name": author}
    footer = ask("Footer", "Footer text (optional): ")
    if footer:
        embed["footer"] = {"text": footer}
    image = ask("Image", "Large image URL (optional): ")
    if image:
        embed["image"] = {"url": image}
    thumb = ask("Thumbnail", "Thumbnail URL (optional): ")
    if thumb:
        embed["thumbnail"] = {"url": thumb}

    embed.setdefault("fields", [])
    while True:
        _render(embed, entries)
        name = input("   Field name (blank to finish): ").strip()
        if not name:
            break
        value = input("   Field value: ").strip()
        inline = input("   Inline? [y/N]: ").strip().lower() in ("y", "yes")
        embed["fields"].append({"name": name, "value": value or "​", "inline": inline})
    if not embed["fields"]:
        del embed["fields"]

    _render(embed, entries)
    if not embed:
        print("   Empty embed, nothing to build.")
        return
    print("\n\033[0;97mEmbed JSON:\033[0m")
    print(json.dumps({"embeds": [embed]}, indent=2, ensure_ascii=False))
    _send(embed)
