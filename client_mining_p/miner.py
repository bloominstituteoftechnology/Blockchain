import hashlib
import requests

import sys
import json

LOTSOFZEROS = 6


PURPLE = "\033[95m"
CYAN ="\033[96m"
DARKCYAN = "\033[36m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END = "\033[0m"


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    block_string = json.dumps(block, sort_keys=True)
    proof = 0
    print("Mining started, please wait.")
    while valid_proof(block_string, proof) is False:
        proof += 1
    print("Mining complete!")
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
    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:LOTSOFZEROS] == '0' * LOTSOFZEROS


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    coins = 0
    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data_received = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print(f"Response returned: {r} ")
            break

        # TODO: Get the block from `data_received` and use it to look for a new proof
        block_data = data_received['last_block']
        
        # last block info 
        print(GREEN + f'1) Last block received: {block_data }!')

        new_proof = proof_of_work(block_data) 

        # found a proof
        print(RED + f'2) new proof received {new_proof }!')

        # adding to /chain
        print('Posting to server.')

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data_received = {"proof": new_proof, "id": id}

        # prints out post data
        print(BOLD + f'3) post data received {post_data_received }!')

        r = requests.post(url=node + "/mine", json=post_data_received)

        # prints response received  plus total coins mined
        print(YELLOW + f'4) response received {r }!')


        data_received = r.json()

        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if data_received['message'] == 'New Block Forged':
            coins += 1
            print(f"{id} received 1 coin. You now have {coins} coin(s)")
        else:
            print(CYAN + f"Try Again")
