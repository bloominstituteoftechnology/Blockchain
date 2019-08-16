import hashlib
import requests

import sys

# things our blockchain is missing 
# 


# TODO: Implement functionality to search for a proof 
def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    """
    print("starting work on a new proof")

    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1
        print("sending to server...")
    return proof

def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?
    """

    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    beg = guess_hash[0:6]

    if beg == "000000":
        return True
    else:
        return False

    # TODO
    # pass

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and 
        # generate a request with last_proof
        req = requests.get(node+'/last_proof', params = params)

        # look for a new one
        new_proof = proof_of_work(req)


        # TODO: When found, POST it to the server {"proof": new_proof}
        data = {
            'proof':new_proof
        }
        
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        r = requests.post(url = node+'/mine', data = data)
        data = r.json()
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        
        if data.get('message') == "New Block Forged":
            coins_mined += 1
            print("you have: " + str(coins_mined) + " coins")

        print(data.get('message'))
        
        
        # print(r.message)
        # print the message from the server.
        pass

# should be able to continously searching for new proofs and display 