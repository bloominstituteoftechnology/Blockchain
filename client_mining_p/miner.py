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
    block_string = json.dumps(block, sort_keys=True)

    proof = 0

    while valid_proof(block_string, proof) == False:
        proof += 1
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
    # print(f"is {proof} valid?")
    guess = block_string + str(proof)
    guess = guess.encode()

    hash_value = hashlib.sha256(guess).hexdigest()
    # print(hash_value)

    # return hash_value[:6] == '000000'
    return hash_value[:4] == '0000'


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    coins_mined = 0
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
            print(data)
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            # returns error and what it did get
            print(r)
            break

        # TODO: Get the block from `data` and use it to look for a new proof
        # new_proof = ???
        print('looking for good proof of work')
        new_proof = proof_of_work(data['last_block'])
        print("got the new proof: ", new_proof)

        # When found, POST it to the server {"proof": new_proof, "id": id}

        # commented out until see what we get from above
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        if 'block' in data:
            # we succeeded
            coins_mined += 1
            print(f"total coins/blocks mined: {coins_mined}")
            time.sleep(1)
        else:
            print(data['message'])

        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        pass
