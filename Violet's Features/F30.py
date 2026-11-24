"""Looks up a card's BIN/IIN (the first 6 to 8 digits) to show the card
scheme (Visa/Mastercard/...), type (debit/credit), brand, the issuing bank
and the country, via the free binlist.net service. Enter only the first 6-8
digits, never a full card number. Use this on YOUR OWN cards or for fraud
checks only; the BIN identifies the bank, not any person or account.
"""
import json
import urllib.error
import urllib.request


def F30():
    print("\033[0;95m== BIN Lookup ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    raw = input("First 6-8 digits (BIN): ").strip().replace(" ", "")
    if not raw.isdigit() or not 6 <= len(raw) <= 8:
        print("Enter 6 to 8 digits only (not a full card number).")
        return
    url = "https://lookup.binlist.net/" + raw
    request = urllib.request.Request(
        url, headers={"User-Agent": "VioletTools/1.0", "Accept-Version": "3"})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            print("BIN not found in the database.")
        elif error.code == 429:
            print("Rate limited by binlist.net, wait a while and retry.")
        else:
            print("Lookup failed:", error)
        return
    except Exception as error:
        print("Lookup failed:", error)
        return
    bank = data.get("bank") or {}
    country = data.get("country") or {}
    print(f"\n\033[0;97mScheme:\033[0m   {data.get('scheme', '-')}")
    print(f"\033[0;97mType:\033[0m     {data.get('type', '-')}")
    print(f"\033[0;97mBrand:\033[0m    {data.get('brand', '-')}")
    print(f"\033[0;97mPrepaid:\033[0m  {data.get('prepaid', '-')}")
    print(f"\033[0;97mBank:\033[0m     {bank.get('name', '-')}")
    if bank.get("url") or bank.get("phone"):
        print(f"\033[0;97mBank info:\033[0m {bank.get('url', '')} {bank.get('phone', '')}".rstrip())
    print(f"\033[0;97mCountry:\033[0m  {country.get('emoji', '')} {country.get('name', '-')}".strip())
