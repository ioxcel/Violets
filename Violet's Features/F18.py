"""Checks an image for data hidden the simple way: extra bytes tacked on
AFTER the real end of the image, and known file signatures (ZIP, PDF, RAR,
etc.) buried inside it -- a classic trick for smuggling files past a glance.
It reports where the image should end, how many trailing bytes follow, and
any embedded file headers it recognises, then offers to carve the hidden
tail out to a file. This is signature/structure analysis, not deep stego.
"""
import os

SIGNATURES = {
    b"PK\x03\x04": "ZIP / Office / APK",
    b"Rar!\x1a\x07": "RAR archive",
    b"7z\xbc\xaf\x27\x1c": "7-Zip archive",
    b"%PDF": "PDF document",
    b"\x1f\x8b\x08": "GZIP",
    b"BZh": "BZIP2",
    b"\xff\xd8\xff": "JPEG image",
    b"\x89PNG\r\n\x1a\n": "PNG image",
    b"GIF8": "GIF image",
    b"ID3": "MP3 audio",
    b"\x7fELF": "ELF executable",
    b"MZ": "DOS/Windows executable",
}


def _image_end(data):
    if data[:2] == b"\xff\xd8":
        idx = data.rfind(b"\xff\xd9")
        return ("JPEG", idx + 2) if idx != -1 else ("JPEG", None)
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        idx = data.rfind(b"IEND")
        return ("PNG", idx + 8) if idx != -1 else ("PNG", None)
    if data[:4] == b"GIF8":
        idx = data.rfind(b"\x3b")
        return ("GIF", idx + 1) if idx != -1 else ("GIF", None)
    return (None, None)


def F18():
    print("\033[0;95m== Stego Detector ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    path = input("Image path: ").strip().strip('"').strip("'")
    if not os.path.isfile(path):
        print("Not a file.")
        return
    with open(path, "rb") as handle:
        data = handle.read()
    kind, end = _image_end(data)
    print(f"\n\033[0;97mFormat:\033[0m       {kind or 'unknown (not JPEG/PNG/GIF)'}")
    print(f"\033[0;97mFile size:\033[0m    {len(data)} bytes")
    trailing = b""
    if end is not None:
        print(f"\033[0;97mImage ends at:\033[0m {end} bytes")
        trailing = data[end:]
        if trailing.strip(b"\x00\r\n "):
            print(f"\033[0;91mTrailing data:\033[0m {len(trailing)} extra bytes after the image!")
        else:
            print("\033[0;97mTrailing data:\033[0m none")
    print("\n\033[0;97mEmbedded signatures:\033[0m")
    hits = []
    for sig, label in SIGNATURES.items():
        start = 8 if label in ("PNG image", "JPEG image", "GIF image") else 1
        pos = data.find(sig, start)
        while pos != -1:
            hits.append((pos, label))
            pos = data.find(sig, pos + 1)
    for pos, label in sorted(hits)[:25]:
        flag = "  \033[0;91m<- inside/after image\033[0m" if end and pos >= end else ""
        print(f"  offset {pos}: {label}{flag}")
    if not hits:
        print("  none found")
    if trailing.strip(b"\x00\r\n ") and input("\nCarve trailing data to a file? [y/N]: ").strip().lower() in ("y", "yes"):
        out = path + ".tail"
        with open(out, "wb") as handle:
            handle.write(trailing)
        print(f"Wrote {len(trailing)} bytes to {out}")
