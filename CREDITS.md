# Credits and Third-Party Licenses

Violet's is released under a proprietary license (see `LICENSE`). The
components below are **not** covered by that license and remain under the
terms of their respective owners.

## Username Search site data — `Violet's Features/sherlock_sites.json`

The Username Search tool uses a bundled site database derived from the
**Sherlock Project**. This data is distributed under the MIT License and is
included here under its terms. The tool only *reads* this file as data; it is
never executed.

> MIT License
>
> Copyright (c) 2018-2023 Sherlock Project
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.

Project: https://github.com/sherlock-project/sherlock

## Public services used at runtime

Several tools query public endpoints. Only the lookup term you enter is sent;
no account, credential or personal detail is transmitted.

| Tool | Service |
| --- | --- |
| IP / Domain Lookup | ip-api.com |
| Subdomain Finder | crt.sh |
| DNS Records | dns.google |
| Wayback Machine | archive.org |
| Pwned Password | api.pwnedpasswords.com (k-anonymity) |
| Geolocator / Photo Geotag | nominatim.openstreetmap.org |
| MAC Vendor | api.macvendors.com |
| BIN Lookup | lookup.binlist.net |
| Discord tools | discord.com public API |

Each service is subject to its own terms of use.
