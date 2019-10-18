import hashlib
import requests

import sys
import json

from uuid import uuid4


def proof_of_work(block):
    """
    Find a number p such that hash(last_block, p) contains 6 leading
    zeroes
    """
    pass


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?
    """
    pass


if __name__ == '__main__':
    # What port is the server on? IE `python3 miner.py 5001`
    if len(sys.argv) > 1:
        node = f'http://localhost:{int(sys.argv[1])}
    else:
        node = "http://localhost:5000"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()
    if len(id) == 0:
        f = open("my_id.txt", "w")
        # Generate a globally unique ID
        id = str(uuid4()).replace('-', '')
        print("Created new ID: " + id)
        f.write(id)
        f.close()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_block")
        data = r.json()
        new_proof = proof_of_work(data.get('last_block'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
