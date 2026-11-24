"""Option 1 computes the MD5, SHA-1 and SHA-256 of a file, for checking
a download matches its published checksum. Option 2 guesses what kind
of hash a string is from its length. Pick 1 or 2 when asked.
"""
import hashlib
import os

BY_LENGTH = {
    32: ["MD5", "NTLM", "MD4"],
    40: ["SHA-1"],
    56: ["SHA-224"],
    64: ["SHA-256"],
    96: ["SHA-384"],
    128: ["SHA-512"],
}


def _identify():
    value = input("Hash: ").strip()
    if not value:
        print("Nothing given.")
        return
    is_hex = all(c in "0123456789abcdefABCDEF" for c in value)
    if not is_hex:
        print("Not a plain hex hash (could be bcrypt, argon2, base64, etc.)")
        return
    guesses = BY_LENGTH.get(len(value))
    if guesses:
        print(f"Length {len(value)} -> possible: {', '.join(guesses)}")
    else:
        print(f"Length {len(value)}: no common match.")


def _hash_file():
    path = input("File path: ").strip().strip('"').strip("'")
    if not os.path.isfile(path):
        print("Not a file.")
        return
    digests = {name: hashlib.new(name) for name in ("md5", "sha1", "sha256")}
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            for digest in digests.values():
                digest.update(chunk)
    for name, digest in digests.items():
        print(f"  {name:7s}: {digest.hexdigest()}")


def F20():
    print("\033[0;95m== Hashes ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    print("1) Hash a file    2) Identify a hash")
    choice = input("Choose [1/2]: ").strip()
    if choice == "2":
        _identify()
    else:
        _hash_file()
