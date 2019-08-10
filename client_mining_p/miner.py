import hashlib
import requests

import sys

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




if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        r = requests.get(url = node +"/last_proof")
        data = r.json()
        last_proof = data['last_proof']

        new_proof = proof_of_work(last_proof)

        proof_data = {'proof': new_proof}

        r = requests.post(url=node + "/mine", json=proof_data)
        print(r.json()['message'])

        if r.json()['message'] == 'New Block Forged':
            coins_mined += 1
            print('Coins Mineds: ', coins_mined)
