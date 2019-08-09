import hashlib
import requests

import sys


# TODO: Implement functionality to search for a proof 
def proof_of_work(last_proof):
    proof = 0
    while not self.valid_proof(last_proof, proof):
        proof += 1

    # for block 1 hash (1, p) = 000000xx
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    """

    def valid_proof(last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        hash_guess = hashlib.sha3_256(guess).hexdigest()
        check = hash_guess[0:4]
        # print(hash_guess)
        if check == '000':
            return True
        else:
            return False
        # """
        # Validates the Proof:  Does hash(block_string, proof) contain 6
        # leading zeroes?
        # """
        # TODO
        pass

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
        proof_of_work()
        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        pass
