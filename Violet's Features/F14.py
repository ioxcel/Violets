"""Turns a place name into coordinates, or coordinates back into an address
(reverse geocoding), using OpenStreetMap's free Nominatim service. Type a
place like 'Eiffel Tower, Paris' to get its latitude/longitude, or type
'lat, lon' like '48.8584, 2.2945' to get the address there. Prints a map
link either way. Nominatim asks for light use, so run one lookup at a time.
"""
import json
import re
import urllib.error
import urllib.parse
import urllib.request

COORD = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*$")


def _get(url):
    request = urllib.request.Request(url, headers={"User-Agent": "VioletTools/1.0 (OSINT lookup)"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def F14():
    print("\033[0;95m== Geolocator ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    query = input("Place name, or 'lat, lon': ").strip()
    if not query:
        print("Enter a place or coordinates.")
        return
    match = COORD.match(query)
    try:
        if match:
            lat, lon = match.group(1), match.group(2)
            url = "https://nominatim.openstreetmap.org/reverse?" + urllib.parse.urlencode(
                {"lat": lat, "lon": lon, "format": "json"})
            data = _get(url)
            if "error" in data:
                print("Nothing found at those coordinates.")
                return
            print(f"\n\033[0;97mAddress:\033[0m  {data.get('display_name', '-')}")
            print(f"\033[0;97mType:\033[0m     {data.get('type', '-')} ({data.get('category', '-')})")
            print(f"\033[0;97mMap:\033[0m      https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=16/{lat}/{lon}")
        else:
            url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
                {"q": query, "format": "json", "limit": "5", "addressdetails": "0"})
            results = _get(url)
            if not results:
                print("No matches.")
                return
            for item in results:
                lat, lon = item["lat"], item["lon"]
                print(f"\n\033[0;97m{item.get('display_name', '-')}\033[0m")
                print(f"  {float(lat):.6f}, {float(lon):.6f}   ({item.get('type', '-')})")
                print(f"  https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=16/{lat}/{lon}")
    except Exception as error:
        print("Lookup failed:", error)
