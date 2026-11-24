"""Resolves a name to an IP, does a reverse lookup, and shows the
country, city, ISP and rough coordinates for that IP (via the free
ip-api.com service). Enter a domain or an IP address.
"""
import json
import socket
import urllib.request


def F3():
    print("\033[0;95m== IP / Domain Lookup ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    target = input("IP or domain: ").strip()
    if not target:
        print("Nothing given.")
        return
    try:
        ip = socket.gethostbyname(target)
    except OSError as error:
        print("Could not resolve:", error)
        return
    print("Resolved IP :", ip)
    try:
        print("Reverse DNS:", socket.gethostbyaddr(ip)[0])
    except OSError:
        print("Reverse DNS: (none)")
    fields = "status,message,country,regionName,city,isp,org,as,lat,lon,timezone"
    url = f"http://ip-api.com/json/{ip}?fields={fields}"
    try:
        with urllib.request.urlopen(url, timeout=8) as response:
            data = json.load(response)
    except Exception as error:
        print("Geo lookup failed:", error)
        return
    if data.get("status") != "success":
        print("Lookup failed:", data.get("message", "unknown"))
        return
    for key in ("country", "regionName", "city", "isp", "org", "as", "timezone"):
        if data.get(key):
            print(f"  {key:10s}: {data[key]}")
    if data.get("lat") is not None:
        print(f"  {'coords':10s}: {data['lat']}, {data['lon']}")
