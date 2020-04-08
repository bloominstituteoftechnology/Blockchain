import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request, render_template


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []       
        self.new_block(previous_hash=1, proof=100) # Create the genesis block

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
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
        string_block = json.dumps(block, sort_keys=True)
        raw_hash = hashlib.sha256(string_block.encode())

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
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:3] =='000'


# Instantiate our Node, unique address and blockchain:
app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

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
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


# @app.route('/')
# def homepage():
#     return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
