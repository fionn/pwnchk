#!/usr/bin/env python3

import requests
import getpass
from hashlib import sha1

def query_pw(prefix):
    assert len(prefix) == 5
    api_url = "https://api.pwnedpasswords.com/range/{}"
    return requests.get(api_url.format(prefix)).iter_lines()

def number_of_hits(pw):
    prefix = pw[:5]
    for line in query_pw(prefix):
        if pw == prefix + line.decode().split(":")[0]:
            return int(line.decode().split(":")[1])
    return 0

if __name__ == "__main__":
    pw = sha1(getpass.getpass().encode()).hexdigest().upper()
    hits = number_of_hits(pw)
    if hits:
        print("{} appears {} times".format(pw, hits))
    else:
        print("No matches")

