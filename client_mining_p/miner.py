# Paste your version of blockchain.py from the basic_block_gp folder here

import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
import sys

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.new_block(proof=100, previous_hash=1)

    def new_block(self, proof, previous_hash=None):
   

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
     
        # TODO: Create the block_string
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object
        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256(block_string.encode())
        hex_hash = raw_hash.hexdigest()

    
        return hex_hash

    @property
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

        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:6] == "000000"

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['POST'])
def mine():

    values = request.get_json()
    required = ['proof', 'id']

    if not all(k in values for k in required):
        response = {'message': 'Missing Required Values'}
        return jsonify(response), 400

    submitted_proof = values.get('proof')
    # Check to see if the proof is valid.
    last_block = blockchain.last_block
    last_block_string = json.dumps(last_block, sort_keys=True)

    if blockchain.valid_proof(last_block_string, submitted_proof):
        # Forge New Block
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(submitted_proof, previous_hash)

        response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        }
        return jsonify(response), 200
    else:
        response = {'message': 'Invalid Proof'}
        return jsonify(response), 400

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'length': len(blockchain.chain),
        'chain': blockchain.chain,
    }
    return jsonify(response), 200

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello world</h1>", 200


@app.route('/last_block', methods=['GET'])
def last_block():
    response = {
        'last_block': blockchain.last_block
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)