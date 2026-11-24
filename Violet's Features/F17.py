"""Scans a file (any file, but handy on images) for human-readable text
hidden inside its bytes, like the classic 'strings' tool. It pulls out
runs of printable characters and then highlights anything that looks like a
URL, email address, file path or key, which is where secrets and clues tend
to hide. Enter a file path and an optional minimum length (default 4).
"""
import os
import re

PRINTABLE = re.compile(rb"[\x20-\x7e]{%d,}")
URL = re.compile(r"https?://[^\s'\"]+")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PATH = re.compile(r"(?:[A-Za-z]:\\|/)[\w./\\-]{4,}")
KEYISH = re.compile(r"(?i)(?:api[_-]?key|secret|token|password|passwd|AKIA[0-9A-Z]{16})")


def F17():
    print("\033[0;95m== Image Strings ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    path = input("File path: ").strip().strip('"').strip("'")
    if not os.path.isfile(path):
        print("Not a file.")
        return
    raw = input("Minimum length [4]: ").strip() or "4"
    minimum = int(raw) if raw.isdigit() and int(raw) >= 1 else 4
    with open(path, "rb") as handle:
        data = handle.read()
    strings = [m.group().decode("ascii") for m in re.finditer(PRINTABLE % minimum, data)]
    if not strings:
        print("No printable strings found.")
        return
    text = "\n".join(strings)
    urls = sorted(set(URL.findall(text)))
    emails = sorted(set(EMAIL.findall(text)))
    paths = sorted(set(PATH.findall(text)))
    secrets = sorted({s for s in strings if KEYISH.search(s)})

    def section(title, items):
        if items:
            print(f"\n\033[0;97m{title} ({len(items)}):\033[0m")
            for item in items[:40]:
                print("  " + item)
            if len(items) > 40:
                print(f"  ... and {len(items) - 40} more")

    section("URLs", urls)
    section("Emails", emails)
    section("Paths", paths)
    section("Possible secrets", secrets)
    print(f"\n\033[0;90m{len(strings)} strings total. Showing highlights above.\033[0m")
    if input("Dump all strings? [y/N]: ").strip().lower() in ("y", "yes"):
        print("\n".join(strings))
