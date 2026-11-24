"""Looks up the public WHOIS registration record for a domain: the
registrar, when it was created / updated / expires, its nameservers and
status. It talks straight to the WHOIS servers on port 43, first asking
IANA who is authoritative for the TLD, then querying that registry. Enter
a domain like example.com. Some registries hide or rate-limit details.
"""
import socket


def _whois(server, query):
    with socket.create_connection((server, 43), timeout=15) as sock:
        sock.sendall((query + "\r\n").encode())
        chunks = []
        while True:
            data = sock.recv(4096)
            if not data:
                break
            chunks.append(data)
    return b"".join(chunks).decode("utf-8", "replace")


def F5():
    print("\033[0;95m== WHOIS ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    domain = input("Domain (e.g. example.com): ").strip().lower().lstrip("*.").strip()
    if not domain or "." not in domain:
        print("Enter a valid domain.")
        return
    tld = domain.rsplit(".", 1)[-1]
    try:
        referral = _whois("whois.iana.org", tld)
    except Exception as error:
        print("WHOIS lookup failed:", error)
        return
    server = ""
    for line in referral.splitlines():
        if line.lower().startswith("whois:"):
            server = line.split(":", 1)[1].strip()
            break
    if not server:
        print("Could not find a WHOIS server for that TLD.")
        print(referral.strip()[:500])
        return
    print(f"Querying {server} ...")
    try:
        record = _whois(server, domain)
    except Exception as error:
        print("Registry query failed:", error)
        return
    fields = ("registrar", "creation date", "created", "updated date",
              "registry expiry date", "expiry date", "expiration", "name server",
              "domain status", "registrant", "org")
    shown = False
    for line in record.splitlines():
        stripped = line.strip()
        if stripped and stripped.lower().split(":", 1)[0] in fields:
            print("  " + stripped)
            shown = True
    if not shown:
        print(record.strip()[:1500] or "No record returned.")
