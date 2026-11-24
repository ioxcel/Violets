"""Pulls the GPS location out of a photo's EXIF metadata (if the camera or
phone saved one) and tells you where it was taken: the coordinates, the
nearest address via OpenStreetMap, and ready-to-open map links. Enter the
path to a JPEG. Many photos from social media have GPS stripped, so a blank
result is normal; it means no location was stored, not that one was hidden.
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

import F15


def _reverse(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse?" + urllib.parse.urlencode(
        {"lat": f"{lat:.6f}", "lon": f"{lon:.6f}", "format": "json"})
    request = urllib.request.Request(url, headers={"User-Agent": "VioletTools/1.0 (OSINT lookup)"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def F16():
    print("\033[0;95m== Photo Geotag ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    path = input("Image path: ").strip().strip('"').strip("'")
    if not os.path.isfile(path):
        print("Not a file.")
        return
    with open(path, "rb") as handle:
        data = handle.read()
    exif = F15._read_exif(data)
    if exif is None:
        print("Only JPEG files carry GPS EXIF.")
        return
    if not exif or "GPS" not in exif:
        print("No GPS location stored in this photo.")
        if exif.get("DateTimeOriginal"):
            print("Taken:", exif["DateTimeOriginal"])
        return
    lat, lon = exif["GPS"]
    print(f"\n\033[0;97mCoordinates:\033[0m  {lat:.6f}, {lon:.6f}")
    if exif.get("DateTimeOriginal"):
        print(f"\033[0;97mTaken:\033[0m        {exif['DateTimeOriginal']}")
    if exif.get("Model"):
        print(f"\033[0;97mCamera:\033[0m       {exif.get('Make', '')} {exif['Model']}".rstrip())
    try:
        place = _reverse(lat, lon)
        if place.get("display_name"):
            print(f"\033[0;97mAddress:\033[0m      {place['display_name']}")
    except Exception as error:
        print(f"\033[0;97mAddress:\033[0m      (reverse geocode failed: {error})")
    print(f"\033[0;97mGoogle Maps:\033[0m  https://www.google.com/maps?q={lat:.6f},{lon:.6f}")
    print(f"\033[0;97mOSM:\033[0m          https://www.openstreetmap.org/?mlat={lat:.6f}&mlon={lon:.6f}#map=17/{lat:.6f}/{lon:.6f}")
