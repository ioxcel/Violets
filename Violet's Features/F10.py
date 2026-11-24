"""Builds advanced Google search queries ('dorks') that narrow results
to one site, file type or keyword, and prints a clickable search
link for each. It only makes queries; you run them in a browser.
"""
import urllib.parse

TEMPLATES = [
    ("Everything on a site", "site:{site}"),
    ("PDF documents", "site:{site} filetype:pdf"),
    ("Office documents", "site:{site} (filetype:doc OR filetype:docx OR filetype:xls)"),
    ("Open directory listings", 'intitle:"index of" site:{site}'),
    ("Login / admin pages", "site:{site} inurl:(login OR admin OR signin)"),
    ("Config / backup files", "site:{site} (ext:env OR ext:bak OR ext:sql OR ext:log)"),
    ("Keyword on site", "site:{site} intext:{kw}"),
    ("Keyword in title", "intitle:{kw}"),
    ("Keyword in URL", "inurl:{kw}"),
]


def F10():
    print("\033[0;95m== Google Dork Builder ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    print("\033[0;90mBuilds search queries. For research on sites you are allowed to review.\033[0m")
    site = input("Site (optional, e.g. example.com): ").strip() or "example.com"
    kw = input("Keyword (optional): ").strip() or "password"
    for label, template in TEMPLATES:
        query = template.format(site=site, kw=kw)
        link = "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)
        print(f"\n\033[0;97m{label}\033[0m")
        print(f"  {query}")
        print(f"  {link}")
