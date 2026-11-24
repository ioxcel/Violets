"""Reads hidden metadata stored inside a photo: camera make/model, the
date taken, pixel size and GPS location if the camera saved one.
Enter the path to a JPEG (GPS and camera tags) or PNG (size only).
"""
import os
import struct
import time

TYPE_SIZE = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 6: 1, 7: 1, 8: 2, 9: 4, 10: 8, 11: 4, 12: 8}


def _parse_tiff(data):
    if len(data) < 8:
        return {}
    order = data[0:2]
    if order == b"II":
        e = "<"
    elif order == b"MM":
        e = ">"
    else:
        return {}
    if struct.unpack(e + "H", data[2:4])[0] != 42:
        return {}
    ifd0_off = struct.unpack(e + "I", data[4:8])[0]

    def read_ifd(offset):
        entries = {}
        if offset <= 0 or offset + 2 > len(data):
            return entries
        count = struct.unpack(e + "H", data[offset:offset + 2])[0]
        p = offset + 2
        for _ in range(count):
            if p + 12 > len(data):
                break
            tag, typ, cnt = struct.unpack(e + "HHI", data[p:p + 8])
            size = TYPE_SIZE.get(typ, 1) * cnt
            if size <= 4:
                raw = data[p + 8:p + 8 + size]
            else:
                off = struct.unpack(e + "I", data[p + 8:p + 12])[0]
                raw = data[off:off + size]
            entries[tag] = (typ, cnt, raw)
            p += 12
        return entries

    def decode(typ, cnt, raw):
        if typ == 2:
            return raw.split(b"\x00", 1)[0].decode("latin1", "replace")
        if typ == 3:
            return list(struct.unpack(e + "%dH" % cnt, raw[:2 * cnt]))
        if typ == 4:
            return list(struct.unpack(e + "%dI" % cnt, raw[:4 * cnt]))
        if typ == 5:
            return [struct.unpack(e + "II", raw[i * 8:i * 8 + 8]) for i in range(cnt)]
        return raw

    result = {}
    ifd0 = read_ifd(ifd0_off)
    for tag, name in {0x010F: "Make", 0x0110: "Model", 0x0132: "DateTime"}.items():
        if tag in ifd0:
            result[name] = decode(*ifd0[tag])
    if 0x8769 in ifd0:
        off = struct.unpack(e + "I", ifd0[0x8769][2][:4])[0]
        exif = read_ifd(off)
        for tag, name in {0x9003: "DateTimeOriginal", 0xA002: "Width", 0xA003: "Height"}.items():
            if tag in exif:
                result[name] = decode(*exif[tag])
    if 0x8825 in ifd0:
        off = struct.unpack(e + "I", ifd0[0x8825][2][:4])[0]
        gps = read_ifd(off)

        def coord(ref_tag, val_tag):
            if val_tag not in gps:
                return None
            vals = decode(*gps[val_tag])
            if not isinstance(vals, list) or len(vals) < 3:
                return None
            parts = [n / d if d else 0 for n, d in vals[:3]]
            dec = parts[0] + parts[1] / 60 + parts[2] / 3600
            if ref_tag in gps:
                ref = decode(*gps[ref_tag])
                if isinstance(ref, str) and ref.upper() in ("S", "W"):
                    dec = -dec
            return dec

        lat, lon = coord(1, 2), coord(3, 4)
        if lat is not None and lon is not None:
            result["GPS"] = (lat, lon)
    return result


def _read_exif(data):
    if data[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 4 < len(data):
        if data[i] != 0xFF:
            break
        marker = data[i + 1]
        if marker in (0xD9, 0xDA):
            break
        seglen = struct.unpack(">H", data[i + 2:i + 4])[0]
        segment = data[i + 4:i + 2 + seglen]
        if marker == 0xE1 and segment[:6] == b"Exif\x00\x00":
            return _parse_tiff(segment[6:])
        i += 2 + seglen
    return {}


def _dimensions(data):
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return w, h
            if marker in (0xD8, 0xD9):
                i += 2
                continue
            i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    elif data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return w, h
    return None


def F15():
    print("\033[0;95m== Image EXIF ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    path = input("Image path: ").strip().strip('"').strip("'")
    if not os.path.isfile(path):
        print("Not a file.")
        return
    stat = os.stat(path)
    with open(path, "rb") as handle:
        data = handle.read()
    print(f"Size     : {stat.st_size} bytes")
    print(f"Modified : {time.ctime(stat.st_mtime)}")
    size = _dimensions(data)
    if size:
        print(f"Pixels   : {size[0]} x {size[1]}")
    exif = _read_exif(data)
    if exif is None:
        print("EXIF     : (only JPEG files carry EXIF)")
        return
    if not exif:
        print("EXIF     : no EXIF data found")
        return
    for key, value in exif.items():
        if key == "GPS":
            lat, lon = value
            print(f"  GPS      : {lat:.6f}, {lon:.6f}")
            print(f"  Map      : https://www.google.com/maps?q={lat:.6f},{lon:.6f}")
        else:
            print(f"  {key:9s}: {value}")
