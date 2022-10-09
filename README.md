# Nullvad
Interactive script to brute force account #s for a certain commercial VPN. Created to help some people understand the level of entropy in this account number/token system.

Proof of concept, don't try to use this script for unethical purposes, you won't find any working account numbers anyway.

With the number of users they report, and the rate limiting that I've encountered (you can make 2 requests within a period of several minutes before you get 503'ed for a while), it will take you an average of well over 150,000 years to find a single valid account number. At that point you can probably save $6.

## Usage:
- Create and activate a venv if preferred: `python -m venv venv`
  - Activate venv, Linux: `source venv/bin/activate`
  - Activate venv, Windows: `.\venv\Scripts\Activate.ps1` (or activate.bat in CMD)
- Install required modules `pip install -r requirements.txt`
- Run the script: `python -m guesser.py`
- Choose an option: Create new account, account brute force, or brute force with proxy
  - If using a proxy, enter your full proxy URL including scheme i.e. `socks5h://1.2.3.4:4145`
- Enter the number of guesses you want it to make
- After each guess, the script will log the attempted account number in either `goodaccounts.txt` or `bad.txt`, depending on if it was a valid account number or not.
- Deactivate venv if using one: `deactivate`

### To do:

- Integrate sys.argv to enable non-interactive use

#### Known issues:

- Python requests module will throw an exception if your environment doesn't trust the API url's CA when using HTTPS proxy
