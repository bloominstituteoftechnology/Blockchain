import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []       
        self.new_block(previous_hash=1, proof=100) # Create the genesis block

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block)
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the block to chain
        self.chain.append(block)
        # Return the new block
        return self.chain

    def hash(self, block):
        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # Use .encode() to convert Python string into a BYTE string.
        # Sort dict keys or we'll have inconsistent hashes
        string_block = json.dumps(block, sort_keys=True)
        raw_hash = hashlib.sha256(string_block.encode())
        

        # The sha256 function returns the hash in a raw string that includes escaped characters.
        # This can be hard to read, but .hexdigest() converts hash to a string of hexadecimal characters
        hex_hash = raw_hash.hexdigest()
        return hex_hash

    @property 
    def last_block(self): #O(1)
        return self.chain[-1]

    def proof_of_work(self, block):
        block_string = json.dumps(block, sort_keys=True)
        proof = 0
        while self.valid_proof(block_string, proof): #until num proof is found
            proof += 1
        return proof

    @staticmethod
    def valid_proof(block_string, proof):
        guess = f'{block_string}{proof}'
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:3] =='000'


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # Run the proof of work algorithm to get the next proof
    # Forge the new Block by adding it to the chain with the proof
    proof = blockchain.proof_of_work(blockchain.last_block)
    previous_hash = blockchain.hash(blockchain.last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'new_block': block
    }

    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'message': 'hello'
        'chain': blockchain.chain,
        'length': len(blockchain.chain)'
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
