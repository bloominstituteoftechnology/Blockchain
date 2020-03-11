import hashlib
import requests

import sys
import json


def proof_of_work(block):
    block_string = json.dumps(block, sort_keys=True)
    proof = 0
    while self.valid_proof(block_string, proof): #until num proof is found
        proof += 1
    return proof


def valid_proof(block_string, proof):
    guess = f'{block_string}{proof}'
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:6] =='000000'


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID -- ID FOR WHAT? WHAT HAS AN ID???
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    # Run until interrupted, and handle non-json response:
    while True:
        r = requests.get(url=node + "/last_block")
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: Get block from `data` and use it to look for a new proof
        new_proof = data.blockchain.proof_of_work(blockchain.last_block) #gets next proof: same thing??


        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        coins = 0
        if message = 'New Block Forged':
            coins += 1
            response = {'coins': coins}
            return jsonify(response)
        else: 
            return jsonify(message)

