# Nullvad
Interactive script to brute force account #s for a certain commercial VPN. Created to help some people understand the level of entropy in this account number system.

Proof of concept, don't try to use this script for unethical purposes, you won't find any working account numbers anyway.

With the number of users they report, and the rate limiting that I've encountered (you can make 2 requests within a several minute period), by my math it will take you an average of well over 150,000 years to find a single valid account number. Or if you hit every one of their servers, at the max rate allowed, you'll have a shiny new VPN account in only about 200 years. At that point you can probably save $6.

To do:

- Use context managers for file I/O
- Add proxy functionality
- Use sys.argv for command line use

Known issues:

- Script unnecessarily waits the full cooldown time when number of guesses is set to 1
