"""Sends a few test packets to a host and reports whether it replies
and how long each round trip takes. Good for 'is it online?' and
rough latency. Enter a domain (example.com) or an IP address.
"""
import platform
import subprocess


def F1():
    print("\033[0;95m== Ping ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    host = input("Host or IP: ").strip()
    if not host:
        print("No host given.")
        return
    flag = "-n" if platform.system() == "Windows" else "-c"
    try:
        result = subprocess.run(["ping", flag, "4", host], text=True,
                                capture_output=True, timeout=30)
    except FileNotFoundError:
        print("The 'ping' command was not found on this system.")
        return
    except subprocess.TimeoutExpired:
        print("Ping timed out.")
        return
    print(result.stdout or result.stderr or "(no output)")
