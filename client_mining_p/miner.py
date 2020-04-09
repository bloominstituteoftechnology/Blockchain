import hashlib
import requests

import sys
import json

"""
step 1: get last block from server
step 2: initiate proof of work process
step 3: when proof is found, call mine endopoint and send proof
step 4: get positive response (receive 1 coin), or failure (go back to step 1 because successful proof may have already been submitted and a new block generated, so we have to get that latest block. The one we have is now the one before last.)
"""


def proof_of_work(block):

    print("proof of work process starting")
    block_string = json.dumps(block["last_block"], sort_keys=True)
    proof = 0
    while not block.valid_proof(block_string, proof):
        proof += 1
    return proof, "proof of work process is finished"


def valid_proof(block_string, proof):
    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:6] == "000000"


if __name__ == "__main__":
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

    # Run forever until interrupted
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
        new_proof = proof_of_work(data)

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        # TODO: If the server responds with a 'message' 'New Block Forged'
        coins = 0
        if data["message"] == "New Block Forged":
            coins += 1
            print(f"coins: {coins}")
        else:
            print(data["message"])
