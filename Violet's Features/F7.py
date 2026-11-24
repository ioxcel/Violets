"""Finds subdomains of a domain by reading public certificate transparency
logs (crt.sh). Every TLS certificate ever issued is logged there, which
quietly reveals hostnames. Enter a domain like example.com. crt.sh can be
slow or rate-limited, so give it a moment.
"""
import json
import urllib.error
import urllib.request


def F7():
    print("\033[0;95m== Subdomain Finder ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    domain = input("Domain (e.g. example.com): ").strip().lower().lstrip("*.").strip()
    if not domain or "." not in domain:
        print("Enter a valid domain.")
        return
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    print("Querying certificate transparency logs (crt.sh) ...")
    request = urllib.request.Request(url, headers={"User-Agent": "VioletTools"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            rows = json.load(response)
    except Exception as error:
        print("Lookup failed (crt.sh can be slow or rate-limited):", error)
        return
    subs = set()
    for row in rows:
        for field in ("name_value", "common_name"):
            for name in str(row.get(field, "")).split("\n"):
                name = name.strip().lstrip("*.").lower()
                if name and name.endswith(domain):
                    subs.add(name)
    subs.discard(domain)
    if not subs:
        print("No subdomains found.")
        return
    for name in sorted(subs):
        print("  " + name)
    print(f"\n\033[0;97m{len(subs)} unique subdomains.\033[0m")
