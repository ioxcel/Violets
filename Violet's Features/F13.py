"""Tells you whether a password has appeared in known data breaches, so you
know to stop using it. It is safe: the password is SHA-1 hashed locally and
only the first 5 characters of that hash are sent (k-anonymity), so the
service never sees your password or its full hash. Type when prompted; input
is hidden. Check YOUR OWN passwords only.
"""
import getpass
import hashlib
import urllib.error
import urllib.request


def F13():
    print("\033[0;95m== Pwned Password Checker ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    try:
        password = getpass.getpass("Password (hidden): ")
    except Exception:
        password = input("Password: ")
    if not password:
        print("Nothing entered.")
        return
    digest = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = digest[:5], digest[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    request = urllib.request.Request(
        url, headers={"User-Agent": "VioletTools", "Add-Padding": "true"})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode()
    except Exception as error:
        print("Lookup failed:", error)
        return
    count = 0
    for line in body.splitlines():
        candidate, _, number = line.partition(":")
        if candidate.strip() == suffix:
            count = int(number)
            break
    if count:
        print(f"\n\033[0;91m[!] Seen in {count:,} breaches. Do not use this password.\033[0m")
    else:
        print("\n\033[0;92m[+] Not found in any known breach.\033[0m")
    print("\033[0;90mOnly the first 5 hash characters left your machine.\033[0m")
