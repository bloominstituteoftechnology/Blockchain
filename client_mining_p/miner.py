import hashlib
import requests
import json
import sys

def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    :return: A valid proof for the provided block
    """
    block_string = json.dumps(block, sort_keys=True).encode()

    proof = 0
    while not self.valid_proof(block_string, proof):
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
        guess = f"{block_string}{proof}".encode()

        guess_hash = hashlib.sha256(guess).hexdigest()
        # TODO: change back to six
        # sys.stdout.write(guess_hash[:3] + " ")
        return guess_hash[:3] == "000"



# TODO: Implement functionality to search for a proof 


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5001"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        print("loopin")
        # TODO: Get the last block from the server and look for a new one
        r = requests.get(url = node + "/last_block")
        last_block = r.json()
        # TODO: When found, POST it to the server {"proof": new_proof}
        new_proof = proof_of_work(last_block['last_block'])

        print(f"found proof and submitting it: {new_proof}")
        post_data = {"proof": new_proof}
        r = requests.post(url=node+"/mine", json=post_data)
        data = r.json()
        print(data)


        # HINT: Research `requests` and remember we're sending our data as JSON
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        pass
