import hashlib
import requests

import sys

from time import time

# TODO: Implement functionality to search for a proof 
def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    """
    start = time()
    print("Starting proof...", end=" ")
    proof = 0

    while valid_proof(last_proof, proof) is False:
        proof += 1

    total_time = time() - start
    print(f"Done in {total_time}.")
    return proof


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?
    """
    # Build string to hash
    guess = f'{last_proof}{proof}'.encode()

    # Hash the string
    guess_hash = hashlib.sha256(guess).hexdigest()

    # Check if 6 leading 0's 
    beg = guess_hash[0:6]
    
    if beg == "000000":
        return True
    
    return False


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        last_proof = requests.get(url = node + '/last_proof').json()
        print(f"Last proof is: {last_proof['last_proof']}")
        new_proof = proof_of_work(last_proof)

        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        data = { 'proof': new_proof }
        r = requests.post(url = node + "/mine", data = data ).json()

        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        print(r)
        if r.get('message') == "New Block Forged":
            coins_mined += 1

        print(f"{r.get('message')} : Total coins is {coins_mined}")
