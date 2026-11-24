"""Checks what a single email address reveals: whether the format is valid,
whether its domain can actually receive mail (MX records), whether it is a
known throwaway/disposable provider, and whether a public Gravatar profile
is linked to it. Enter an email address. Nothing is sent to the address.
"""
import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request

DISPOSABLE = {
    "mailinator.com", "guerrillamail.com", "10minutemail.com", "tempmail.com",
    "temp-mail.org", "throwawaymail.com", "yopmail.com", "getnada.com",
    "trashmail.com", "maildrop.cc", "fakeinbox.com", "sharklasers.com",
    "dispostable.com", "mohmal.com", "emailondeck.com",
}


def F12():
    print("\033[0;95m== Email Recon ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    email = input("Email address: ").strip()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        print("That does not look like a valid email address.")
        return
    domain = email.rsplit("@", 1)[1].lower()
    print("Format   : valid")
    if domain in DISPOSABLE:
        print("Domain   : \033[0;91mknown disposable / throwaway provider\033[0m")
    else:
        print("Domain   :", domain)
    try:
        doh = f"https://dns.google/resolve?name={urllib.parse.quote(domain)}&type=MX"
        with urllib.request.urlopen(doh, timeout=8) as response:
            answer = json.load(response).get("Answer", [])
        mx = [a["data"] for a in answer if a.get("type") == 15]
    except Exception:
        mx = None
    if mx is None:
        print("MX       : lookup failed")
    elif mx:
        print("MX       : can receive mail ->", ", ".join(sorted(mx)[:3]))
    else:
        print("MX       : no MX records (likely cannot receive mail)")
    digest = hashlib.md5(email.strip().lower().encode()).hexdigest()
    try:
        request = urllib.request.Request(
            f"https://www.gravatar.com/avatar/{digest}?d=404",
            method="HEAD", headers={"User-Agent": "VioletTools"})
        with urllib.request.urlopen(request, timeout=8) as response:
            gravatar = response.status == 200
    except urllib.error.HTTPError as error:
        gravatar = error.code == 200
    except Exception:
        gravatar = None
    if gravatar:
        print(f"Gravatar : \033[0;92mexists\033[0m -> https://gravatar.com/{digest}")
    elif gravatar is False:
        print("Gravatar : none linked")
    else:
        print("Gravatar : check failed")
