# Violet's

A terminal toolkit for network reconnaissance, OSINT, file forensics and
Discord utilities. It runs entirely in the terminal with an animated paged
menu and thirty self-contained tools, written in pure Python with no
third-party dependencies.

## Highlights

- Thirty tools across three themed pages, selected by number from the menu.
- No external packages required — only the Python standard library.
- Cross-platform: Linux, macOS and Windows (launches its own terminal window,
  or runs in place with `--show`).
- Every tool opens with an information panel explaining what it does and how
  to use it.
- Tools act only on the targets you supply, and online lookups send nothing
  beyond the term you enter.

## Tools

**Network & Web** — Ping, Port Scanner, IP / Domain Lookup, DNS Records,
WHOIS, SSL Inspector, Subdomain Finder, Website Info, Wayback Machine,
Google Dork Builder.

**OSINT & Forensics** — Username Search, Email Recon, Pwned Password,
Geolocator, Image EXIF, Photo Geotag, Image Strings, Stego Detector,
Reverse Image Search, Hashes.

**Discord / Identity & Metadata** — Snowflake Decoder, Invite Inspector,
Webhook Inspector, Webhook Tester, Embed Builder, Phone Lookup, MAC Vendor,
PDF Metadata, Password Tools, BIN Lookup.

## Requirements

- **Python 3.8 or newer** — standard library only, no `pip install` needed.
- A terminal with ANSI colour support (truecolor recommended).
- The system `ping` command, used by the Ping tool (present by default on
  Windows, macOS and Linux).
- An internet connection for the online lookup tools.

These are also listed in [`requirements.txt`](requirements.txt).

## Usage

```
python3 violets.py
```

This opens a new terminal window and draws the menu. Use the left and right
arrow keys to move between pages, type a tool number into the `Value:` prompt
and press Enter to run it, and press `Esc` to exit.

To run inside the current terminal instead of opening a new window:

```
python3 violets.py --show
```

## Project layout

```
violets.py              Launcher, menu, animation and dispatch
Violet's Features/      One module per tool (F1.py ... F30.py)
  sherlock_sites.json   Site data for the Username Search tool
```

## Credits

See [CREDITS.md](CREDITS.md) for third-party data attribution (including the
Sherlock Project site database) and the public services used at runtime.

## License

Copyright (c) 2026 Matas. All rights reserved. This project is published for
reference only; see [LICENSE](LICENSE) for the terms. It may not be copied,
reused, modified or redistributed without written permission.
