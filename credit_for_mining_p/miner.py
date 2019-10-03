import hashlib
import requests

import sys
import uuid

# def load_id():
#     text_file = open('my_id.txt', 'r')
#     my_id = text_file.read().split(',')
#     text_file.close()
#     return my_id

# def save_id():
#     text_file = open('my_id.txt', 'r')
#     text_file.write( str(id))
#     text_file.close()

def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 6 leading
    zeroes, where p is the previous p
    - p is the previous proof, and p' is the new proof
    """

    print("Searching for next proof")
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    print("Proof found: " + str(proof))
    return proof


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 6
    leading zeroes?
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    breakpoint()
    return guess_hash[:6] == "000000"

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = int(sys.argv[1])
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Open persistent data of ids to see if id is there
    # If no id, create one using uuid, and save to file
    f = open('my_id.txt', 'r')
    id = f.read()
    f.close()

    if len(id) == 0:
        print("Miner ID not found, creating Miner ID ...")
        f = open("my_id.txt", "w")
        id = str(uuid.uuid1()).replace('-', '')
        print("New Miner ID saved: " + id)
        f.write(id)
        f.close()
    print('Miner ID located: ', id)
    
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {
            "proof": new_proof,
            "id": id
        }

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
