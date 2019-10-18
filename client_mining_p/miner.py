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

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    # Run forever until interrupted
    while True:
        # TODO: Get the last block from the server and look for a new proof
        # TODO: When found, POST it to the server {"proof": new_proof, "id": id}
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        pass
