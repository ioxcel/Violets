"""Connects to a site over TLS and shows its SSL certificate: who it was
issued to, who issued it, how long it is valid, the serial and SHA-256
fingerprint, and every hostname it covers (the SAN list). Enter a hostname
like example.com (optionally host:port; default port is 443). It reads the
certificate the server presents and changes nothing.
"""
import hashlib
import socket
import ssl
from datetime import datetime, timezone


def _name(pairs):
    out = {}
    for rdn in pairs:
        for key, value in rdn:
            out[key] = value
    return out


def F6():
    print("\033[0;95m== SSL Inspector ==\033[0m")
    print("\033[0;90m" + __doc__.strip() + "\033[0m\n")
    target = input("Host (e.g. example.com or host:443): ").strip()
    if not target:
        print("Enter a hostname.")
        return
    host, _, port = target.partition(":")
    host = host.replace("https://", "").strip("/")
    try:
        port = int(port) if port else 443
    except ValueError:
        print("Invalid port.")
        return
    context = ssl.create_default_context()
    try:
        with socket.create_connection((host, port), timeout=15) as raw:
            with context.wrap_socket(raw, server_hostname=host) as tls:
                cert = tls.getpeercert()
                der = tls.getpeercert(binary_form=True)
                cipher = tls.cipher()
    except ssl.SSLCertVerificationError as error:
        print(f"Certificate did NOT verify: {error.verify_message}")
        print("(Reading it anyway is not supported here; the chain is untrusted.)")
        return
    except Exception as error:
        print("Connection failed:", error)
        return
    subject = _name(cert.get("subject", []))
    issuer = _name(cert.get("issuer", []))
    fmt = "%b %d %H:%M:%S %Y %Z"
    not_after = datetime.strptime(cert["notAfter"], fmt).replace(tzinfo=timezone.utc)
    days_left = (not_after - datetime.now(timezone.utc)).days
    print(f"\n\033[0;97mSubject:\033[0m     {subject.get('commonName', '-')}")
    print(f"\033[0;97mIssuer:\033[0m      {issuer.get('organizationName', issuer.get('commonName', '-'))}")
    print(f"\033[0;97mValid from:\033[0m  {cert.get('notBefore', '-')}")
    print(f"\033[0;97mValid to:\033[0m    {cert.get('notAfter', '-')}  ({days_left} days left)")
    if days_left < 0:
        print("  \033[0;91m** EXPIRED **\033[0m")
    print(f"\033[0;97mSerial:\033[0m      {cert.get('serialNumber', '-')}")
    print(f"\033[0;97mSHA-256:\033[0m     {hashlib.sha256(der).hexdigest()}")
    print(f"\033[0;97mCipher:\033[0m      {cipher[0]} ({cipher[1]}, {cipher[2]} bit)")
    sans = [value for key, value in cert.get("subjectAltName", []) if key == "DNS"]
    if sans:
        print(f"\033[0;97mSANs ({len(sans)}):\033[0m")
        for name in sans:
            print("  " + name)
