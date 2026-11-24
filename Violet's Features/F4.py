"""Dumps the public DNS records for a domain -- A and AAAA (addresses),
MX (mail servers), NS (nameservers), TXT (SPF/verification), CNAME and
SOA. It uses Google's DNS-over-HTTPS resolver, so it works anywhere HTTPS
does, with no DNS tools installed. Enter a domain like example.com.
"""
import json
import urllib.error
import urllib.parse
import urllib.request

RECORDS = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]
TYPE_NAME = {1: "A", 28: "AAAA", 15: "MX", 2: "NS", 16: "TXT", 5: "CNAME", 6: "SOA"}


def _query(domain, record):
    url = "https://dns.google/resolve?" + urllib.parse.urlencode({"name": domain, "type": record})
    request = urllib.request.Request(url, headers={"User-Agent": "VioletTools/1.0"})
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)


def F4():
    print("\033[0;95m== DNS Records ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    domain = input("Domain (e.g. example.com): ").strip().lower().strip(". ")
    if not domain or "." not in domain:
        print("Enter a valid domain.")
        return
    found = False
    for record in RECORDS:
        try:
            data = _query(domain, record)
        except Exception as error:
            print(f"\033[0;97m{record}\033[0m: lookup failed ({error})")
            continue
        answers = [a for a in data.get("Answer", []) if TYPE_NAME.get(a.get("type")) == record]
        if not answers:
            continue
        found = True
        print(f"\n\033[0;97m{record}\033[0m")
        for answer in answers:
            print(f"  {answer.get('data', '').strip()}  \033[0;90m(ttl {answer.get('TTL', '?')})\033[0m")
    if not found:
        print("No records found (or the domain does not resolve).")
