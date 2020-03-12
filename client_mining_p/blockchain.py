# Paste your version of blockchain.py from the basic_block_gp
# folder here

import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # create the genesis block
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
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'current_transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block)
        }
        self.current_transactions = []
        self.chain.append(block)

        return block

    def hash(self,block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        string_block = json.dumps(block, sort_keys=True)
        raw_hash = hashlib.sha256(string_block.encode())
        hex_hash = raw_hash.hexdigest()

        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

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
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:6] == "000000"

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/last_block', methods=['GET'])
def last_block():
    response = {
        'last_block': blockchain.last_block
    }
    return jsonify(response), 200


@app.route('/mine', methods=['POST'])
def mine():
    # Run the proof of work algorithm to get the next proof
    # sent by client
    # pull out the data
    data = requeest.get_json()
    # check if both are passed in
    required = ['proof', 'id']
    # if we do not get everything in required, we give an error
    if not all(k in data for k in required):
        response = {'message': 'Missing values'}
        return jsonify(response), 400

    last_block = blockchain.last_block
    last_string = json.dumps(last_block, sort_keys=True
    )
    if blockchain.valid_proof(last_string, data['proof']):
        # we add the new block to the chain by hasing it
        previous_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.new_block(data['proof'], previous_hash)

        reponse = {
            'message': 'New Block Forged',
            'new_block': block

        }
    else:
        response ={
            'message': 'Invalid Proof!'

        }
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
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
