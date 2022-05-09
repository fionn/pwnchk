#!/usr/bin/env python3
"""Check if your password has been pwned"""

import sys
import getpass
import argparse
from hashlib import sha1
from typing import Iterator

import requests

class PwnChk:
    """Check if your password has been pwned"""

    def __init__(self, padding: bool = True) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "pwnchk-alpha",
                                     "Add-Padding": str(padding).lower()})
        self.public_api_url = "https://api.pwnedpasswords.com/range/"

    def _get(self, url: str) -> requests.models.Response:
        response = self.session.get(url)
        response.raise_for_status()
        return response

    @staticmethod
    def hash(string: str) -> str:
        """Helper to hash a password"""
        return sha1(string.encode()).hexdigest()

    def query_pw(self, prefix: str) -> Iterator[bytes]:
        """Send hash prefix to API and get an iterator of the response"""
        assert len(prefix) == 5
        return self._get(self.public_api_url + prefix).iter_lines()

    def hits(self, pw_hash: str) -> int:
        """Frequency of occurrances"""
        pw_hash = pw_hash.upper()
        prefix = pw_hash[:5]
        for line in self.query_pw(prefix):
            if pw_hash == prefix + line.decode().split(":")[0]:
                return int(line.decode().split(":")[1])
        return 0

def main() -> None:
    """Entry point"""

    parser = argparse.ArgumentParser(description="Check if your password has been pwned")
    parser.add_argument("--stdin", action="store_true", help="read from stdin")
    parser.add_argument("--no-padding", action="store_true",
                        help="don't add random padding to the response")
    args = parser.parse_args()

    if args.stdin:
        password = sys.stdin.read().strip()
    else:
        password=getpass.getpass()

    pwnchk = PwnChk(padding=(not args.no_padding))

    pw_hash = pwnchk.hash(password)
    hits = pwnchk.hits(pw_hash)

    if hits:
        print(f"{pw_hash} appears {hits} times")
    else:
        print(f"{pw_hash} does not appear")

if __name__ == "__main__":
    main()
