"""Checks which TCP ports are open on a host, which hints at what
services it runs (22=SSH, 80/443=web, etc). Enter a host, then a
range like 1-1024 or a single port. Only scan machines you own
or have permission to test.
"""
import socket
from concurrent.futures import ThreadPoolExecutor

COMMON = {
    20: "ftp-data", 21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp",
    53: "dns", 80: "http", 110: "pop3", 143: "imap", 443: "https",
    445: "smb", 3306: "mysql", 3389: "rdp", 5432: "postgres",
    6379: "redis", 8080: "http-alt", 8443: "https-alt",
}


def _check(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.6)
            if s.connect_ex((host, port)) == 0:
                return port
    except OSError:
        return None
    return None


def F2():
    print("\033[0;95m== Port Scanner ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    print("\033[0;90mOnly scan hosts you own or are authorised to test.\033[0m")
    host = input("Host or IP: ").strip()
    if not host:
        print("No host given.")
        return
    rng = input("Port range [1-1024]: ").strip() or "1-1024"
    try:
        if "-" in rng:
            a, b = rng.split("-", 1)
            start, end = int(a), int(b)
        else:
            start = end = int(rng)
    except ValueError:
        print("Bad port range.")
        return
    start, end = max(1, start), min(65535, end)
    if end < start:
        print("Bad port range.")
        return
    try:
        ip = socket.gethostbyname(host)
    except OSError as error:
        print("Could not resolve host:", error)
        return
    print(f"Scanning {ip} ports {start}-{end} ...")
    ports = range(start, end + 1)
    with ThreadPoolExecutor(max_workers=200) as pool:
        found = [p for p in pool.map(lambda port: _check(ip, port), ports) if p]
    if not found:
        print("No open ports found.")
        return
    for port in sorted(found):
        print(f"  {port:5d}  open   {COMMON.get(port, '')}")
