#!/usr/bin/env python3

import getpass
from hashlib import sha1
from typing import Generator
import requests

def query_pw(prefix: str) -> Generator[bytes, None, None]:
    assert len(prefix) == 5
    api_url = "https://api.pwnedpasswords.com/range/{}"
    return requests.get(api_url.format(prefix)).iter_lines()

def number_of_hits(pw_hash: str) -> int:
    prefix = pw_hash[:5]
    for line in query_pw(prefix):
        if pw_hash == prefix + line.decode().split(":")[0]:
            return int(line.decode().split(":")[1])
    return 0

def main() -> None:
    pw_hash = sha1(getpass.getpass().encode()).hexdigest().upper()
    hits = number_of_hits(pw_hash)
    if hits:
        print("{} appears {} times".format(pw_hash, hits))
    else:
        print("No matches")

if __name__ == "__main__":
    main()

