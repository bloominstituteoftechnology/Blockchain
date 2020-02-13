import hashlib
import requests
import sys
import json
import time


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    start = time.time()
    block_string = json.dumps(block, sort_keys=True)
    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1
    end = time.time()
    timer = end - start
    print(f'Runtime: {timer} seconds')
    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
        
    return guess_hash[:6] == "000000"


class User:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.transactions = []

    def change_name(self, new_name):
        self.name = new_name
        return f'\nYou have changed your name to {self.name}\n'

    def get_balance(self):
        return f"\n{self.name} has {self.balance} coin(s).\n"

    def get_transactions(self):
        return f"\n{self.name} transaction's: {self.transactions}\n"


if __name__ == '__main__':
    confirm = True
    while confirm == True:
        name = input("Enter your name: ")
        confirmation = input(f'Are you sure you want your name to be {name}?')
        if (confirmation == 'y'):
            newUser = User(name)
            confirm = False
    # Prints a message to confirm creation of new user
    print(f"\nNew user created for {newUser.name}!\n")
    # Asks the user what it would like to do
    next_input = str(input("What would you like to do:\n Change name(1)\n Get balance(2)\n Get transactions(3)\n Make transaction(4)\n Mine for coin(5)\n or Quit(q)?"))
    # Loops forever until user enters q
    while True:
        if (next_input == '1'):
            new_name = str(input('\nWhat would you like to change your name to?\n'))
            print(newUser.change_name(new_name))
            next_input = str(input("What would you like to do:\n Change name(1)\n Get balance(2)\n Get transactions(3)\n Make transaction(4)\n Mine for coin(5)\n or Quit(q)?"))

        elif (next_input == '2'):
            print(newUser.get_balance())
            next_input = str(input("What would you like to do:\n Change name(1)\n Get balance(2)\n Get transactions(3)\n Make transaction(4)\n Mine for coin(5)\n or Quit(q)?"))

        elif (next_input == '3'):
            print(newUser.get_transactions())
            next_input = str(input("What would you like to do:\n Change name(1)\n Get balance(2)\n Get transactions(3)\n Make transaction(4)\n Mine for coin(5)\n or Quit(q)?"))

        elif (next_input == '4'):
            recip = input("\nWho is the recipient?\n")
            amount = input("\nHow many coins do you want to send?\n")

            while (int(amount) > newUser.balance):
                print("You don't have enough coins.")
                amount = input("\nHow many coins do you want to send?\n")

            post_data = {"sender": newUser.name, "recipient": recip, "amount": amount}
            r = requests.post(url=node + '/transaction/new', json=post_data)
            data = r.json()
            print('\n' + data['message'] + '\n')

            newUser.transactions.append({'sender': newUser.name, 'recipient': recip, 'amount': int(amount), 'index': data['message']})

            next_input = str(input("What would you like to do:\n Change name(1)\n Get balance(2)\n Get transactions(3)\n Make transaction(4)\n Mine for coin(5)\n or Quit(q)?"))

        elif (next_input == '5'):
            node = "http://127.0.0.1:5000"
            coins_mined = 0
            while True:
                r = requests.get(url=node + "/last_block")
                # Handle non-json response
                try:
                    data = r.json()
                except ValueError:
                    print("Error:  Non-json response")
                    print("Response returned:")
                    print(r)
                    break

                # TODO: Get the block from `data` and use it to look for a new proof
                new_proof = proof_of_work(data['last_block'])

                # When found, POST it to the server {"proof": new_proof, "id": username}
                print(f'Id is {newUser.name}')
                post_data = {"proof": new_proof, "id": newUser.name}

                r = requests.post(url=node + "/mine", json=post_data)
                data = r.json()

                # TODO: If the server responds with a 'message' 'success'
                # add 1 to the number of coins mined and print it.  Otherwise,
                # print the message from the server.
                if (data['message'] == 'Success'):
                    newUser.balance += 1
                    coins_mined += 1
                    print(f'You have mined {coins_mined} coin(s). This round.')
                else:
                    print(data['message'])
                stop = input("\n Would you like to stop mining?(y/n)\n")
                if (stop.lower() == 'y'):
                    break
            next_input = str(input("What would you like to do:\n Change name(1)\n Get balance(2)\n Get transactions(3)\n Make transaction(4)\n Mine for coin(5)\n or Quit(q)?"))

        elif (next_input.lower() == 'q'):
            break

        else:
            print('You did not give a proper input. Try again...')
            next_input = str(input("What would you like to do:\n Change name(1)\n Get balance(2)\n Get transactions(3)\n Make transaction(4)\n Mine for coin(5)\n or Quit(q)?"))
