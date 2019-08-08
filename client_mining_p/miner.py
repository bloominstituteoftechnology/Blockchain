import hashlib
import requests

import sys


# Implement functionality to search for a proof 
def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    """
    print("Starting")
    proof = 0
    # for block 1, hash(1,p) = 000000x
    while valid_proof(last_proof, proof) is False :
        proof += 1
    print("Sending to server...")    
    return proof   

def valid_proof(last_proof, proof):
    """
    Validates the Proof:  
    Does hash(block_string, proof)
    contain 6 leading zeroes?
    """
    #build string to hash
    guess = f'{last_proof}{proof}'.encode()
    #use hash function
    guess_hash = hashlib.sha256(guess).hexdigest()
    # check if 6 leading 0's
    beg = guess_hash[0:6] # [:6]
    if beg == "000000":
        return True
    else:
        return False

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # Get the last proof from the server and look for a new one
        # r = requests.get(url = node + "/last_proof")
        #DO not need to use r.json(), but its good to use
       

        new_proof = proof_of_work(last_proof)
        data = {'proof': new_proof}
        # Assign our new_proof to 'proof'
        proof_data = {'proof': new_proof}

        # requests.post to /mine endpoint
        r = requests.post(url = node + '/mine', data = data)

        if r.message == 'New Block Forged':
            coins_mined += 1
            print('Coines mined: ', coins_mined)
