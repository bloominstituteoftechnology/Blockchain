import hashlib
import requests

import json

import sys


def proof_of_work(last_block):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    """

    block_string = json.dumps(last_block, sort_keys=True).encode()
    proof = 0
    while not valid_proof(block_string, proof):
        proof += 1

    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?
    """

    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    # TODO:  CHANGE BACK TO SIX!!!!!!!!!
    return guess_hash[:4] == "0000"


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        data = r.json()
        last_block = data['last_block']
        print("Last block is:")
        print(last_block)
        new_proof = proof_of_work(last_block)
        print(f"found a proof: {new_proof}")

        post_data = {
            "proof": new_proof
        }

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        if data['message'] == "New Block Forged":
            # keep track of the coins we've mined
            print(data['message'])
        else:
            print("handle failure message")

        # TODO: Get the last proof from the server and look for a new one
        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        pass
