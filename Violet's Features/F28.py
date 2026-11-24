"""Extracts the hidden metadata from a PDF: title, author, subject,
keywords, the software that created it (Creator/Producer), and the creation
and modification dates. These often reveal the real author's name, their
username, or the tool/version used. Enter the path to a .pdf. It reads the
document information dictionary and XMP packet from the raw file (no PDF
libraries), so some heavily compressed files may show only partial data.
"""
import os
import re

FIELDS = ["Title", "Author", "Subject", "Keywords", "Creator", "Producer",
          "CreationDate", "ModDate"]


def _decode_pdf_string(raw):
    if raw.startswith(b"<") and raw.endswith(b">"):
        hexs = re.sub(rb"[^0-9A-Fa-f]", b"", raw[1:-1])
        if len(hexs) % 2:
            hexs += b"0"
        try:
            text = bytes.fromhex(hexs.decode())
            if text[:2] in (b"\xfe\xff", b"\xff\xfe"):
                return text.decode("utf-16", "replace")
            return text.decode("latin1", "replace")
        except Exception:
            return raw.decode("latin1", "replace")
    body = raw[1:-1] if raw.startswith(b"(") else raw
    body = re.sub(rb"\\([nrtbf()\\])", lambda m: {
        b"n": b"\n", b"r": b"\r", b"t": b"\t", b"b": b"\b", b"f": b"\f",
        b"(": b"(", b")": b")", b"\\": b"\\"}[m.group(1)], body)
    if body[:2] in (b"\xfe\xff", b"\xff\xfe"):
        return body.decode("utf-16", "replace")
    return body.decode("latin1", "replace")


def _pdf_date(value):
    m = re.match(r"D?:?(\d{4})(\d{2})?(\d{2})?(\d{2})?(\d{2})?(\d{2})?", value)
    if not m:
        return value
    y, mo, d, h, mi, s = (p or "" for p in m.groups())
    out = y
    if mo:
        out += f"-{mo}"
    if d:
        out += f"-{d}"
    if h:
        out += f" {h}:{mi or '00'}:{s or '00'}"
    return out


def F28():
    print("\033[0;95m== PDF Metadata ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    path = input("PDF path: ").strip().strip('"').strip("'")
    if not os.path.isfile(path):
        print("Not a file.")
        return
    with open(path, "rb") as handle:
        data = handle.read()
    if not data.startswith(b"%PDF"):
        print("That is not a PDF file.")
        return
    print(f"\033[0;97mPDF version:\033[0m  {data[1:8].decode('latin1', 'replace')}")
    found = False
    for field in FIELDS:
        match = re.search(rb"/" + field.encode() + rb"\s*(\([^)]*\)|<[0-9A-Fa-f\s]*>)", data)
        if not match:
            continue
        value = _decode_pdf_string(match.group(1)).strip()
        if not value:
            continue
        found = True
        if field in ("CreationDate", "ModDate"):
            value = _pdf_date(value)
        print(f"\033[0;97m{field + ':':13s}\033[0m {value}")
    xmp = re.search(rb"<x:xmpmeta.*?</x:xmpmeta>", data, re.DOTALL)
    if xmp:
        tags = re.findall(rb"<(dc:creator|xmp:CreatorTool|pdf:Producer|dc:title)[^>]*>(.*?)</",
                          xmp.group(), re.DOTALL)
        shown = set()
        for tag, val in tags:
            text = re.sub(rb"<[^>]+>", b"", val).decode("utf-8", "replace").strip()
            key = tag.decode()
            if text and key not in shown:
                shown.add(key)
                if not found:
                    print("\033[0;90m-- from XMP --\033[0m")
                    found = True
                print(f"\033[0;97m{key + ':':13s}\033[0m {text}")
    if not found:
        print("No metadata found (document info may be compressed or stripped).")
