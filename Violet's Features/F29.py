"""A small password toolkit: generate a strong random password, build a
memorable passphrase from random words, or estimate how strong a password
you already have is (its entropy in bits and rough crack time). Pick an
option when prompted. Everything runs locally with Python's cryptographic
'secrets' generator, so nothing you type or generate ever leaves the machine.
"""
import math
import secrets
import string

GUESSES_PER_SECOND = 100_000_000_000

WORDS = ("amber anchor apple arrow autumn basil beacon birch bison blaze "
         "bramble breeze bronze canyon cedar cherry cinder clover cobalt comet "
         "copper coral cosmic crimson crystal dagger dawn delta drift ember "
         "falcon fern flint forest galaxy garnet ginger glacier granite harbor "
         "hazel heron indigo ivory jade jasper jungle kelp lagoon lantern "
         "lemon lilac lotus lunar maple marble meadow meteor mint nebula "
         "nickel oak ocean olive onyx opal orbit otter pebble pepper pine "
         "pixel plum quartz quill raven reef river rowan ruby saffron sage "
         "sapphire shadow silver slate solar spruce storm summit thistle "
         "thunder tiger topaz tundra umber velvet walnut willow zephyr").split()


def _entropy(pw):
    pool = 0
    if any(c.islower() for c in pw):
        pool += 26
    if any(c.isupper() for c in pw):
        pool += 26
    if any(c.isdigit() for c in pw):
        pool += 10
    if any(c in string.punctuation for c in pw):
        pool += len(string.punctuation)
    if any(c not in string.printable for c in pw):
        pool += 100
    return len(pw) * math.log2(pool) if pool else 0


def _crack_time(bits):
    seconds = (2 ** bits) / 2 / GUESSES_PER_SECOND
    for unit, size in (("years", 31557600), ("days", 86400), ("hours", 3600),
                       ("minutes", 60), ("seconds", 1)):
        if seconds >= size:
            return f"{seconds / size:,.1f} {unit}"
    return "instant"


def _rate(bits):
    if bits < 40:
        return "\033[0;91mvery weak\033[0m"
    if bits < 60:
        return "\033[0;91mweak\033[0m"
    if bits < 80:
        return "\033[0;93mfair\033[0m"
    if bits < 110:
        return "\033[0;92mstrong\033[0m"
    return "\033[0;92mvery strong\033[0m"


def F29():
    print("\033[0;95m== Password Tools ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    print("  [1] Random password")
    print("  [2] Passphrase")
    print("  [3] Check a password's strength")
    choice = input("Choose [1/2/3]: ").strip()
    if choice == "1":
        raw = input("Length [20]: ").strip() or "20"
        length = int(raw) if raw.isdigit() and 4 <= int(raw) <= 256 else 20
        symbols = input("Include symbols? [Y/n]: ").strip().lower() not in ("n", "no")
        alphabet = string.ascii_letters + string.digits + (string.punctuation if symbols else "")
        pw = "".join(secrets.choice(alphabet) for _ in range(length))
        bits = _entropy(pw)
        print(f"\n\033[0;97m{pw}\033[0m")
        print(f"\033[0;90mentropy ~{bits:.0f} bits ({_rate(bits)}\033[0;90m)\033[0m")
    elif choice == "2":
        raw = input("Number of words [5]: ").strip() or "5"
        count = int(raw) if raw.isdigit() and 2 <= int(raw) <= 12 else 5
        sep = input("Separator [-]: ").strip() or "-"
        words = [secrets.choice(WORDS) for _ in range(count)]
        phrase = sep.join(words) + str(secrets.randbelow(100)).zfill(2)
        bits = count * math.log2(len(WORDS))
        print(f"\n\033[0;97m{phrase}\033[0m")
        print(f"\033[0;90mentropy ~{bits:.0f} bits from words ({_rate(bits)}\033[0;90m)\033[0m")
    elif choice == "3":
        pw = input("Password to check: ")
        if not pw:
            print("Nothing entered.")
            return
        bits = _entropy(pw)
        print(f"\n\033[0;97mLength:\033[0m   {len(pw)}")
        print(f"\033[0;97mEntropy:\033[0m  ~{bits:.0f} bits  ({_rate(bits)}\033[0m)")
        print(f"\033[0;97mCrack:\033[0m    ~{_crack_time(bits)} at 100B guesses/sec (offline)")
        print("\033[0;90mRough estimate. A password in a breach list is weak at any length.\033[0m")
    else:
        print("Pick 1, 2 or 3.")
