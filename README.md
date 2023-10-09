# Nullvad

Automatically brute force account #s for a certain commercial VPN.

Don't use this script for unethical purposes, you won't find any working account numbers anyway. This was made to prove that point; if you want to use it, just buy it.

## Usage:
- Optional: Create a venv if preferred: `python3 -m venv venv`
  - Activate venv, Linux: `source venv/bin/activate`
  - Activate venv, Windows Powershell: `.\venv\Scripts\Activate.ps1`
  - Activate venv, Windows cmd: `.\venv\Scripts\activate.bat`
- Install required modules: `pip install -r requirements.txt`
- Run the script: `python3 nullvad.py --proxy socks5://myproxy:4145`
- The script will start making requests to the [VPN provider redacted] accounts API endpoint and print the results of each. It will log each attempted account number in either `goodaccounts.txt` or `bad.txt`, depending on whether or not the account is valid. If running on Windows, will also send a notification upon finding a valid account.

The rate limiting in place on the API endpoint is somewhat dynamic. To maximize your requests, hit it in bursts of 5-10 requests, one request per 10-20 seconds, then stop for a bit. If you hit it faster than that, you'll start getting 503'ed after only 2 requests. I've incorporated an automatic 60 second pause when the script sees that you're getting 503'ed, so it will mostly take care of these bursts for you unattended. If you want to leave it running for extended periods, i.e. forever, without getting rate limited then you're better off setting --ratelimit to 300 seconds or so, so that you're just hitting it once every few minutes. If you set it lower than that, you'll eventually start getting 503's again.

## Command line arguments, all optional:
- `-r` / `--ratelimit` - Rate limit in seconds. Default: 30
- `-p` / `--proxy` - Proxy URL. Include scheme, i.e. `-p socks5h://1.2.3.4:4145` Default: none
- `-g` / `--guesses` - Number of guesses to make before quitting. Default: Infinite
- `-n` / `--newaccount` - Create new account
## Note
Shout out to this VPN for being one of the only commercial VPNs worth buying.
