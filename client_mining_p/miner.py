import hashlib
import requests

import sys


# TODO: Implement functionality to search for a proof

def valid_proof(last_proof, proof):
    guess = f"{last_proof}{proof}".encode()
    hash_guess = hashlib.sha3_256(guess).hexdigest()
    check = hash_guess[0:6]
    # print(hash_guess)
    if check == '00000':
        return True
    else:
        return False
    # """
    # Validates the Proof:  Does hash(block_string, proof) contain 6
    # leading zeroes?
    # """
    # TODO
    pass

def proof_of_work(last_proof):
    proof = 0
    print(f"Starting new proof: {proof}")
    while not valid_proof(last_proof, proof):
        proof += 1
    print('Sending to server.')
    return proof

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one

        # TODO: Use get request to send/get back new proof?

        r_get = requests.get(url= node + '/last_block_proof', data=None)
        info = r_get.json()

        new_proof = proof_of_work(last_proof)

        data = { 'proof': new_proof }

        r = requests.post(url=node+'/mine', data=data)

        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        # TODO: If the server responds with 'New Block Forged'

        if r.message == "New Block Forged":
            coins_mined += 1
            print(f"You have {coins_mined} coins.")
        print(r.message)
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
