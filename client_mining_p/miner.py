import hashlib
import requests

import sys
import json


@property
def last_block(self):
    return self.chain[-1]

def proof_of_work(block):
    
    # Simple Proof of Work Algorithm
    # Stringify the block and look for a proof
    block_string = json.dumps(block, sort_keys=True)
    # proof with 6 leading zeros
    proof = 000000
    # Loop through possibilities, checking each one against `valid_proof`
    while valid_proof(block_string, proof) is False:
        proof += 1  
    # in an effort to find a number that is a valid proof
    # :return: A valid proof for the provided block
    
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
    return guess_hash[:6] == "000000"



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
    coins_mined = 0

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
        block = data['last_block']
        print('Success')
        print('Starting proof')
        # new_proof = ???
        new_proof = proof_of_work(data['last_block'])
        # new_proof  = proof_of_work(block)
        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        try:
            data = r.json()
            if data['message'] == 'New Block Forged':
                coins_mined += 1
            print(f'Success!  {coins_mined}')
            print(data)
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        
