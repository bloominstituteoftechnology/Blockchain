import hashlib
import requests

import sys
import json
import time
import random


def proof_of_work(block, iterations, difficulty):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    blockString = json.dumps(block, sort_keys=True)
    for i in range(iterations):
        proof = int(random.random() * 100000000)
        if valid_proof(blockString, proof, difficulty):
            return proof
    return None


def valid_proof(block_string, proof, difficulty):
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
    guessHash = hashlib.sha256(guess).hexdigest()
    return guessHash[:difficulty] == "0" * difficulty


def getLastblock():
    r = requests.get(url=node + "/lastblock")
    diff = requests.get(url=node + "/difficulty")
    # Handle non-json response
    try:
        data = r.json()
        difficulty = diff.json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(r)
        return None

    return (data, difficulty)

def submitProof(new_proof):
    # When found, POST it to the server {"proof": new_proof, "id": id}
    post_data = {"proof": new_proof, "id": id}

    r = requests.post(url=node + "/mine", json=post_data)
    try:
        data = r.json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(r)
    status = data.get("status", None)
    if status is not None:
        if status == "success":
            return True
        else:
            print("block already solved")
            return False
    else:
        return False

if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    # if len(sys.argv) > 1:
    #     node = sys.argv[1]
    # else:
    node = "http://localhost:5000"

    # Load ID
    if len(sys.argv) > 1:
        id = sys.argv[1]
    else:
        f = open("my_id.txt", "r")
        id = f.read()
        f.close()

    print("ID is", id)

    coins = 0

    # Run forever until interrupted
    while True:
        data = None
        new_proof = None
        while new_proof is None:
            data, difficulty = getLastblock()
            if data is None:
                break
            new_proof = proof_of_work(data, 1000000, difficulty)

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        success = submitProof(new_proof)
        if success:
            coins += 1
            print(f"my coins: {coins}")
