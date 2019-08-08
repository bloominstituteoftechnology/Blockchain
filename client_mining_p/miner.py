import hashlib
import requests

import sys


# TODO: Implement functionality to search for a proof 
def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?
    """
    #String to hash
    guess = f'{last_proof}{proof}'.encode()
    #Hash string
    guess_hash = hashlib.sha256(guess).hexdigest()
    #check for 6 leading 0s
    beg = guess_hash[:5]
    return beg == '00000'

def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    """
    proof = 0

    while valid_proof(last_proof, proof) is False:
        proof += 1
    print('Sending to server....')
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
        last_proof = requests.get(url = node+'/last_proof').json()
        new_proof = proof_of_work(last_proof['last_proof'])
        # TODO: When found, POST it to the server {"proof": new_proof}

        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        data = {'proof': new_proof}
        r = requests.post(url = node+'/mine', data = data)
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        print(r)
        # print the message from the server.
        # if r['message'] == 'New Block Forged':
        #     print('yay')
        # else:
        #     print('ugh')

