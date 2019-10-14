import hashlib
import requests

import sys
import requests
import json
import time
import hashlib


# TODO: Implement functionality to search for a proof 
def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Find a number p such that ha contains 6 leading
    zeroes
    :return: A valid proof for the provided block
    """
    # TODO
    block_string = json.dumps(block, sort_keys=True).encode()
    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1

    return proof
    # return proof

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
    # TODO
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"
    # return True or False


def hash(block):
    block_string = json.dumps(block, sort_keys=True).encode()

    return hashlib.sha256(block_string).hexdigest()

def new_block(proof, previous_block):
    """
    Create a new Block in the Blockchain

    :param proof: <int> The proof given by the Proof of Work algorithm
    :param previous_hash: (Optional) <str> Hash of previous Block
    :return: <dict> New Block
    """

    block = {
        'index': previous_block["index"] + 1 ,
        'timestamp': time.time(),
        'transactions': [],
        'proof': proof,
        'previous_hash': previous_block["previous_hash"]
    }

    return block

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    index = 2
    while True:
        # TODO: Get the last proof from the server and look for a new one
        response = requests.get(node + "/last_block")


        lastBlock = json.loads(response.text)["last_block"]
        print ("Last block", lastBlock)

        newProofOfWork = proof_of_work(response.text)

        # TODO: When found, POST it to the server {"proof": new_proof}
        newBlock = new_block(newProofOfWork, lastBlock)
        requests.post(node + "/mine", json   = newBlock)
        index += 1

        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        coins_mined += 1
        input("Press any key to continue... ")
        pass
