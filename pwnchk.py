#!/usr/bin/env python3
"""Check if you've been pwned"""

import getpass
import argparse
from hashlib import sha1
from typing import Iterator

import requests

class PwnChk:
    """Check if you've been pwned"""

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
        """Helper to get correctly formatted hash"""
        return sha1(string.encode()).hexdigest().upper()

    def query_pw(self, prefix: str) -> Iterator[bytes]:
        """Send hash prefix to API and get an iterator of the response"""
        assert len(prefix) == 5
        response = self._get(self.public_api_url + prefix)
        return response.iter_lines()

    def number_of_hits(self, pw_hash: str) -> int:
        """Return frequency of occurrances"""
        prefix = pw_hash[:5]
        for line in self.query_pw(prefix):
            if pw_hash == prefix + line.decode().split(":")[0]:
                return int(line.decode().split(":")[1])
        return 0

def main() -> None:
    """Entry point"""

    parser = argparse.ArgumentParser(description="Check if you've been pwned")
    parser.add_argument("--email", type=str, help="not implemented")
    parser.add_argument("--no-padding", action="store_true",
                        help="don't add random padding to the response")
    args = parser.parse_args()

    pwnchk = PwnChk(padding=(not args.no_padding))

    if args.email:
        print("This API isn't public")
    else:
        pw_hash = pwnchk.hash(getpass.getpass())
        hits = pwnchk.number_of_hits(pw_hash)

        if hits:
            print(f"{pw_hash} appears {hits} times")
        else:
            print("No matches")

if __name__ == "__main__":
    main()
