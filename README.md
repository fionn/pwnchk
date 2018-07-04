Check a password against a database of breaches.

This queries the [pwned passwords](https://haveibeenpwned.com/Passwords) API v2. The password never leaves your machine, only a prefix of the SHA1, which guarantees _k_-anonymity.

