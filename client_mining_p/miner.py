import hashlib
import requests

import sys


# Implement functionality to search for a proof 

# if __name__ == '__main__': means
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
        return guess_hash[:4] == "0000"

    # Run forever until interrupted
    while True:
        # Get the last proof from the server and look for a new one
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
            if #'New Block Forged' then coin += 1
            # last_proof = data['proof']
            # print("Last Proof: %s"%(last_proof))
            # new_proof = mine('new proof')
            # coins_mined += 1
            # When found, POST it to the server {"proof": new_proof}
            # r = requests.post(url = node + "/mine", data = data)
            # pastebin_url = r.text 
            # print("The pastebin URL is:%s"%pastebin_url)
            # If the server responds with 'New Block Forged'
            # add 1 to the number of coins mined and print it.  Otherwise,
            # print the message from the server.

