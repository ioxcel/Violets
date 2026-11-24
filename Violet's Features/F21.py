"""Decodes a Discord snowflake ID (user, message, channel, server or
role ID) into the exact date and time it was created, plus the internal
worker, process and increment values Discord packs into every ID. This
is pure maths on the number itself -- nothing is sent anywhere, so it
works offline and reveals nothing the ID did not already contain.
"""
import datetime

EPOCH = 1420070400000


def F21():
    print("\033[0;95m== Snowflake Decoder ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    raw = input("Snowflake ID: ").strip()
    if not raw.isdigit():
        print("Enter a numeric Discord ID (17-20 digits).")
        return
    snowflake = int(raw)
    if snowflake < (1 << 22):
        print("That number is too small to be a Discord snowflake.")
        return
    milliseconds = (snowflake >> 22) + EPOCH
    created = datetime.datetime.fromtimestamp(milliseconds / 1000, datetime.timezone.utc)
    worker = (snowflake >> 17) & 0x1F
    process = (snowflake >> 12) & 0x1F
    increment = snowflake & 0xFFF
    age = datetime.datetime.now(datetime.timezone.utc) - created
    days = age.days
    years = days / 365.25
    print(f"\n\033[0;97mCreated (UTC):\033[0m  {created.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
    print(f"\033[0;97mUnix (ms):\033[0m     {milliseconds}")
    print(f"\033[0;97mAge:\033[0m           {days} days ({years:.2f} years)")
    print(f"\033[0;97mWorker ID:\033[0m     {worker}")
    print(f"\033[0;97mProcess ID:\033[0m    {process}")
    print(f"\033[0;97mIncrement:\033[0m     {increment}")
