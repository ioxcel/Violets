"""Looks up the manufacturer that owns a network device's MAC address by its
OUI (the first three bytes, assigned by the IEEE). Enter a MAC in any common
form -- AA:BB:CC:DD:EE:FF, aa-bb-cc-..., or aabb.ccdd.eeff. It queries the
free macvendors.com API, and also tells you if the address is locally
administered (randomised/spoofed) or a multicast address.
"""
import re
import urllib.error
import urllib.request


def F27():
    print("\033[0;95m== MAC Vendor ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    raw = input("MAC address: ").strip()
    hexonly = re.sub(r"[^0-9A-Fa-f]", "", raw)
    if len(hexonly) < 6:
        print("Enter at least the first 3 bytes of a MAC (the OUI).")
        return
    oui = hexonly[:6].upper()
    pretty = ":".join(oui[i:i + 2] for i in (0, 2, 4))
    first = int(oui[:2], 16)
    print(f"\n\033[0;97mOUI:\033[0m          {pretty}")
    print(f"\033[0;97mLocal/random:\033[0m {'yes (locally administered -- may be spoofed)' if first & 0x02 else 'no (globally unique)'}")
    print(f"\033[0;97mMulticast:\033[0m    {'yes' if first & 0x01 else 'no (unicast)'}")
    url = "https://api.macvendors.com/" + pretty
    request = urllib.request.Request(url, headers={"User-Agent": "VioletTools/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            vendor = response.read().decode("utf-8", "replace").strip()
        print(f"\033[0;97mVendor:\033[0m       {vendor}")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            print("\033[0;97mVendor:\033[0m       not found (unregistered or private OUI)")
        elif error.code == 429:
            print("\033[0;97mVendor:\033[0m       rate limited -- wait a second and retry")
        else:
            print("\033[0;97mVendor:\033[0m       lookup failed:", error)
    except Exception as error:
        print("\033[0;97mVendor:\033[0m       lookup failed:", error)
