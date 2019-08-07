import hashlib
import requests

import sys


# TODO: Implement functionality to search for a proof 


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0

    def valid_proof(last_proof, proof):
        """
        Validates the Proof:  Does hash(last_proof, proof) contain 4
        leading zeroes?
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:6] == "000000"


    # Run forever until interrupted
    while True:
        r = requests.get(url = node + "/last_proof")
        data = r.json()

        proof = 0
        while (valid_proof(data['proof'], proof) is False):
            proof += 1
        post_data = {
            'proof': guess_hash,

        }
        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        # TODO: Get the last proof from the server and look for a new one
        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        pass
