import hashlib  #sha-256 for this project
import json  
from time import time
from uuid import uuid4  # for unique user id  -  very difficult to replicate

from flask import Flask, jsonify, request  # gotta learn about flask


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash="I'm a teapot.", proof=100)

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
        # a dictionary
        block = {
            # TODO
            'index': len(self.chain) + 1, # index of the first block is 1
            # for index here in a block, we get to count normally
            'time_stamp':time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash # or self.hash(self.chain[-1]) hashing the last block
        }

        # Reset the current list of transactions
        self.current_transactions = []
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
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        '''
        # json.dumps ( stringifys json ) 
        # turn block into a string
        #sort_key = True = makes sure keys are done in the same order
            # otherwise they will all be different

        problem with python string = they are actually objects so have to encode

        '''
        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        '''

        look up hexdigest()

        '''

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return hex_hash

    @property # decorator~ the preamble for a function
    # makes the return from the function a property of the chain
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        """
        Simple Proof of Work Algorithm
        Stringify the block and look for a proof.
        Loop through possibilities, checking each one against `valid_proof`
        in an effort to find a number that is a valid proof
        :return: A valid proof for the provided block
        """
        # TODO
        pass
        # return proof

    @staticmethod # decorator
    # can run it without an instance
    def valid_proof(block_string, proof):
        #  hash(block_string, proof) = proof of work
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
        pass
        # return True or False


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()
print(blockchain.chain)
print(blockchain.hash(blockchain.last_block))


@app.route('/mine', methods=['GET']) # get request
def mine():
    # Run the proof of work algorithm to get the next proof

    # Forge the new Block by adding it to the chain with the proof

    response = {
        # TODO: Send a JSON response with the new block
        'message':'Hello Nisa!'
    }

    return jsonify(response), 200


@app.route('/chain', methods=['GET']) # get request
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
