Check a password against a database of breaches.

This queries Troy Hunt's [pwned passwords](https://haveibeenpwned.com/Passwords) API v2. The password never leaves your machine, only a prefix of the SHA1, thereby guaranteeing _k_-anonymity.

