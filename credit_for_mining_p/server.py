import hashlib
import json
from time import time
from uuid import uuid4
import sys

from flask import Flask, jsonify, request
from blockchain import Blockchain

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine/<node_id>', methods=['POST'])
def mine(node_id):
    # We run the proof of work algorithm to get the next proof...
    # proof = blockchain.proof_of_work(blockchain.last_block)
    last_block = blockchain.last_block
    last_block_string = json.dumps(last_block, sort_keys=True).encode()

    values = request.get_json()

    submitted_proof = values['proof']
    
    if not blockchain.valid_proof(last_block_string, submitted_proof):
        response = {
            # TODO: send diefferent message if proof was valid but late.
            'message': 'proof was invalid or submitted too late'
        }
        return jsonify(response, 200)

    # We must receive a reward for finding the proof.

    # The sender is "0" to signify that this node has mine a new coin
    # The recipient is the current node, it did the mining!
    # The amount is 1 coin as a reward for mining the next block
    blockchain.new_transaction(
        sender = "0",
        recipient = node_id,
        amount = 1
    )


    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(blockchain.last_block)
    block = blockchain.new_block(submitted_proof, previous_hash)

    # Send a response with the new block
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        # 'message': f'proof found: {proof}'
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing Values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'],
                                       values['recipient'],
                                       values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain
    }
    return jsonify(response), 200

@app.route('/valid_chain', methods=['GET'])
def validate_chain():
    result = blockchain.valid_chain(blockchain.chain)

    response = {
        'validity': result
    }
    return jsonify(response, 200)

@app.route('/last_block', methods=['GET'])
def get_last_block():
    result = blockchain.chain[-1]

    response = {
        'last_block': result
    }

    return jsonify(response, 200)
    
# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
