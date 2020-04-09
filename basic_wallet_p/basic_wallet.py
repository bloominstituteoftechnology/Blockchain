# Account balances in a blockchain currency are not real values that are stored somewhere. 
#  Instead, wallet programs derive this balance 
# by adding and subtracting all of the transactions 
# for the user that are recorded in the ledger, 
# to calculate the current balance.

# Build a simple wallet app using the front-end technology of your choice.  
# You will not be evaluated on the aesthetics of your app.

# This app should:
#     * Allow the user to enter, save, or change the `id` used for the program
#     * Display the current balance for that user
#     * Display a list of all transactions for this user, including sender and recipient

import hashlib
import requests

import sys
import json
from flask import Flask, jsonify, request


        
    # check for data 
def check_for_data(data):
    try:
        data = data.json()
    except ValueError:
        print(jsonify({'message':'please input your proof'}))
        return
    return data
    
def get_transactions():
    r = requests.get(url=node +"/transactions")
    data = check_for_data(r)
    if data:
        return data['transactions']
    transactions = data['transactions']
    print(f'{transactions.sender}, {transactions.recepient}, {transactions.ammount}')
        
def get_my_transactions(id):
    transactions = get_transactions()
    if transactions:
        my_transactions = []
        for action in transactions:
            if action['recepient'] == id:
                my_transactions.append(action)    
            elif action['sender'] == id:
                my_transactions.append(action)
        return my_transactions
    else:
        print("something went wrong")
        
def get_my_balance(id):
    my_transactions = get_my_transactions(id)
    coins = 0
    for action in my_transactions:
        if action["recepient"] == id:
            coins += action['amount']
        elif action['sender'] == id:
            coins += action['amount']
    print(f'{id}:{coins}')
if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

print(get_transactions())
print(get_my_transactions("albert-yakubov"))    
print(get_my_balance("albert-yakubov"))

        