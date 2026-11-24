"""Fetches a URL and shows the HTTP status, where it redirects to, all
response headers (server software, cookies, etc) and the page title.
Enter a URL; http:// is added if you leave it off.
"""
import re
import urllib.error
import urllib.request


def _show(response):
    print("Status    :", response.status, response.reason)
    print("Final URL :", response.geturl())
    print("Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    return response.read(200000).decode("utf-8", "replace")


def F8():
    print("\033[0;95m== Website Info ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    url = input("URL: ").strip()
    if not url:
        print("No URL given.")
        return
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    request = urllib.request.Request(url, headers={"User-Agent": "VioletTools/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = _show(response)
    except urllib.error.HTTPError as error:
        body = _show(error)
    except Exception as error:
        print("Request failed:", error)
        return
    match = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
    if match:
        print("Title     :", re.sub(r"\s+", " ", match.group(1)).strip())
