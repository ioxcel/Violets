"""Builds reverse-image-search links so you can find where an image appears
online, who else posted it, or the original source. Give it a direct image
URL (one ending in .jpg/.png/etc.) and it generates ready-to-click search
links for Google Lens, Yandex (often best for faces/places), Bing Visual
Search, TinEye and Karma Decay (Reddit). It builds links only -- you open
them in a browser. Searching by a local file means uploading it on the site.
"""
import urllib.parse


def F19():
    print("\033[0;95m== Reverse Image Search ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    url = input("Direct image URL: ").strip()
    if not url.lower().startswith(("http://", "https://")):
        print("Enter a full image URL starting with http:// or https://")
        print("\033[0;90m(For a file on disk, open a site below and use its upload button.)\033[0m")
        return
    quoted = urllib.parse.quote(url, safe="")
    engines = [
        ("Google Lens", f"https://lens.google.com/uploadbyurl?url={quoted}"),
        ("Yandex", f"https://yandex.com/images/search?rpt=imageview&url={quoted}"),
        ("Bing", f"https://www.bing.com/images/search?q=imgurl:{quoted}&view=detailv2&iss=sbi"),
        ("TinEye", f"https://tineye.com/search?url={quoted}"),
        ("Karma Decay (Reddit)", f"http://karmadecay.com/search?q={quoted}"),
    ]
    for name, link in engines:
        print(f"\n\033[0;97m{name}\033[0m")
        print("  " + link)
    print("\n\033[0;90mTip: Yandex is usually strongest for faces, places and landmarks.\033[0m")
