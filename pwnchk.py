#!/usr/bin/env python3
"""Check if you're pwned"""

import getpass
from hashlib import sha1
from typing import Generator
import requests

class PwnChk:
    """Check if you're pwned"""

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "pwnchk-alpha"})
        self.public_api_url = "https://api.pwnedpasswords.com/range/"

    def _get(self, url: str) -> requests.models.Response:
        response = self.session.get(url)
        response.raise_for_status()
        return response

    @staticmethod
    def hash(string: str) -> str:
        """Helper to get correctly formatted hash"""
        return sha1(string.encode()).hexdigest().upper()

    def query_pw(self, prefix: str) -> Generator[bytes, None, None]:
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
    import argparse

    parser = argparse.ArgumentParser(description="Check if you've been pwned")
    parser.add_argument("--email", type=str, help="Not implemented")
    args = parser.parse_args()

    pwnchk = PwnChk()

    if args.email:
        print("This API isn't public")
    else:
        pw_hash = pwnchk.hash(getpass.getpass())
        hits = pwnchk.number_of_hits(pw_hash)

        if hits:
            print("{} appears {} times".format(pw_hash, hits))
        else:
            print("No matches")

if __name__ == "__main__":
    main()
