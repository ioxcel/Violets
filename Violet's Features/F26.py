"""Identifies the country (and likely region) behind an international phone
number from its calling code, fully offline. Enter a number in international
form, e.g. +44 7911 123456 or 0044... or 1-202-555-0143. It matches the
longest dialling-code prefix and shows the country and the national-number
length. It does NOT reveal the carrier, owner or whether the line is mobile
-- that needs a paid lookup service -- so treat this as country ID only.
"""
import re

CODES = {
    "1": "North America (US / Canada / NANP)", "7": "Russia / Kazakhstan",
    "20": "Egypt", "27": "South Africa", "30": "Greece", "31": "Netherlands",
    "32": "Belgium", "33": "France", "34": "Spain", "36": "Hungary",
    "39": "Italy", "40": "Romania", "41": "Switzerland", "43": "Austria",
    "44": "United Kingdom", "45": "Denmark", "46": "Sweden", "47": "Norway",
    "48": "Poland", "49": "Germany", "51": "Peru", "52": "Mexico",
    "53": "Cuba", "54": "Argentina", "55": "Brazil", "56": "Chile",
    "57": "Colombia", "58": "Venezuela", "60": "Malaysia", "61": "Australia",
    "62": "Indonesia", "63": "Philippines", "64": "New Zealand",
    "65": "Singapore", "66": "Thailand", "81": "Japan", "82": "South Korea",
    "84": "Vietnam", "86": "China", "90": "Turkey", "91": "India",
    "92": "Pakistan", "93": "Afghanistan", "94": "Sri Lanka", "95": "Myanmar",
    "98": "Iran", "211": "South Sudan", "212": "Morocco", "213": "Algeria",
    "216": "Tunisia", "218": "Libya", "220": "Gambia", "221": "Senegal",
    "233": "Ghana", "234": "Nigeria", "237": "Cameroon", "243": "DR Congo",
    "249": "Sudan", "250": "Rwanda", "251": "Ethiopia", "254": "Kenya",
    "255": "Tanzania", "256": "Uganda", "260": "Zambia", "263": "Zimbabwe",
    "264": "Namibia", "265": "Malawi", "267": "Botswana", "351": "Portugal",
    "352": "Luxembourg", "353": "Ireland", "354": "Iceland", "355": "Albania",
    "356": "Malta", "357": "Cyprus", "358": "Finland", "359": "Bulgaria",
    "370": "Lithuania", "371": "Latvia", "372": "Estonia", "373": "Moldova",
    "374": "Armenia", "375": "Belarus", "376": "Andorra", "377": "Monaco",
    "380": "Ukraine", "381": "Serbia", "382": "Montenegro", "385": "Croatia",
    "386": "Slovenia", "387": "Bosnia and Herzegovina", "389": "North Macedonia",
    "420": "Czech Republic", "421": "Slovakia", "423": "Liechtenstein",
    "501": "Belize", "502": "Guatemala", "503": "El Salvador", "504": "Honduras",
    "505": "Nicaragua", "506": "Costa Rica", "507": "Panama", "509": "Haiti",
    "591": "Bolivia", "593": "Ecuador", "595": "Paraguay", "598": "Uruguay",
    "852": "Hong Kong",
    "853": "Macau", "855": "Cambodia", "856": "Laos", "880": "Bangladesh",
    "886": "Taiwan", "960": "Maldives", "961": "Lebanon", "962": "Jordan",
    "963": "Syria", "964": "Iraq", "965": "Kuwait", "966": "Saudi Arabia",
    "967": "Yemen", "968": "Oman", "970": "Palestine", "971": "United Arab Emirates",
    "972": "Israel", "973": "Bahrain", "974": "Qatar", "975": "Bhutan",
    "976": "Mongolia", "977": "Nepal", "992": "Tajikistan", "993": "Turkmenistan",
    "994": "Azerbaijan", "995": "Georgia", "996": "Kyrgyzstan", "998": "Uzbekistan",
}


def F26():
    print("\033[0;95m== Phone Lookup ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    raw = input("Phone number (international, e.g. +44...): ").strip()
    digits = re.sub(r"\D", "", raw)
    if raw.startswith("00"):
        digits = digits[2:]
    if not digits:
        print("Enter a phone number.")
        return
    for length in (3, 2, 1):
        prefix = digits[:length]
        if prefix in CODES:
            national = digits[length:]
            print(f"\n\033[0;97mCalling code:\033[0m  +{prefix}")
            print(f"\033[0;97mCountry:\033[0m       {CODES[prefix]}")
            print(f"\033[0;97mNational no.:\033[0m  {national}  ({len(national)} digits)")
            print(f"\033[0;97mE.164:\033[0m        +{digits}")
            print("\n\033[0;90mCountry from dialling code only -- not carrier or owner.\033[0m")
            return
    print("Could not match a country calling code. Include the country code (e.g. +44).")
