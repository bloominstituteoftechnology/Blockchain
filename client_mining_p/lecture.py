import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request

import random
import string


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            "index": len(self.chain) + 1,
            "timestamp":time(),
            "transactions":self.current_transactions,
            "proof":proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]) #or self.lastblock
        }

        # Reset the current list of transactions
        current_transactions = []
        # Append the block to the chain
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        string_block = json.dumps(block, sort_keys=True)#if orders change, the hash would be different
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        raw_hash = hashlib.sha256(string_block.encode())
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes
        hex_hash = raw_hash.hexdigest()

        # TODO: Create the block_string
        return hex_hash

        # TODO: Hash this string using sha256

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        pass

    @property #property decorator, don't need to use 
    #parenthesis when you use this, acts like a property not a method, 
    # gives you the last block
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # TODO

        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest() # turn into a hexadecimal string

        return guess_hash[:3] == '000'#slice off last 6, see if it equals all zeros
        # we compare hexidecimal strings


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
        # values = request.get_json()#could crash server on json on nonjson object
        # required = ['proof', 'id']#runtime complexity is (nested for loop is n^2) but this is constant so O(2n)
        # if not all(k in values for k in required)# for everything in a check everything in b
        # #compare all of one list in list of another
        #     response = {'message':'Missing values'}
        #     return jsonify(response), 400
    block_string = json.dumps(blockchain.last_block, sort_keys=True)
    # send the recipient who mined successfully a reward - 12.5
    if blockchain.valid_proof(block_string, submitted_proof):
        # submitted_proof = values['proof']
        # Run the proof of work algorithm to get the next proof
        # Forge the new Block by adding it to the chain with the proof
        previous_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.new_block(proof, previous_hash)

        response = {
            'new_block': block
        }
        return jsonify(response), 200
    else:
        response = {
            'message':'Proof was invalid or late'
        }
        return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Send a JSON response with the new block
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def get_last_block():
        response = {
            'last_block': blockchain.last_block# we checked miner.py to see if we have to call the key something specifc
        }
        return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

