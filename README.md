# Nullvad
Interactive script to automatically brute force account #s for a certain commercial VPN. Created to help some people understand the level of entropy in this account number/token system. 

Proof of concept, don't try to use this script for unethical purposes, you won't find any working account numbers anyway.

## Usage:
- Create a venv if preferred: `python3 -m venv venv`
  - Activate venv, Linux: `source venv/bin/activate`
  - Activate venv, Windows Powershell: `.\venv\Scripts\Activate.ps1`
- Install required modules: `pip install -r requirements.txt`
- Optional: In the top of the script, set the `COOLDOWN` constant equal to the rate limit you want to follow (in seconds)
- Run the script: `python guesser.py`
- Choose an option: Create new account, account brute force, or brute force with proxy
  - If using a proxy, enter your full proxy URL including scheme i.e. `socks5h://1.2.3.4:4145`
- Enter the number of guesses you want it to make, or 0 to run indefinitely
- The script will start making requests to the [VPN provider name] accounts API endpoint and print the results of each. It will log each attempted account number in either `goodaccounts.txt` or `bad.txt`, depending on whether or not the account is valid. If running on Windows, will also send a notification upon finding a valid account.

The rate limiting in place on the API endpoint seems somewhat dynamic. To maximize your requests, hit it in bursts of 5-10 requests, one request per 10-20 seconds, then stop for a bit. If you hit it faster than that, you'll start getting 503'ed after only 2 requests. I've incorporated an automatic 60 second pause when the script sees that you're getting 503'ed, so it will mostly take care of these bursts for you unattended. If you want to leave it running for extended periods, i.e. forever, without getting rate limited then you're better off setting the COOLDOWN to 300 seconds or so, so that you're just hitting it once every few minutes. If you set it lower than that, you'll eventually start getting 503's again.

### To do:

- Integrate argparse/sys.argv to take command line args for non-interactive use
  - Args to parse:
    - -c COOLDOWN (maybe change this constant's name to RATELIMIT or something more intuitive)
    - -p proxyinput (unspecified = none)
    - num_of_guesses (if unspecified then default infinite)

#### Known issues:

- Requests module will raise an exception if your environment doesn't trust the API endpoint's SSL cert. If you run into this issue, see Python Requests module's docs about verifying certs.
