import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block),
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

    @property #acts like property, not method - don't have to use ()
    def last_block(self): #O(1)
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        guess = f'{block_string}{proof}'
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:6] =='000000'

    def new_transaction(self, sender, recipient, amount): #can't be static, we adding things to current trasnactions
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        #last block is cement, unchangeable, so newest/latest bloack is...
        return self.last_block['index'] + 1 


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    # Handle non json request
    values = request.get_json()

    required = ['proof', 'id']
    if not all(k in values for k in required): #nested for loop, no problem, it's small, O(2n) is constant, linear
        response = {'message': 'Missing values'}
        return jsonify(response), 400

    submitted_proof = values['proof']

    block_string = json.dumps(blockchain.last_block, sort_keys=True)
    if blockchain.valid_proof(block_string, submitted_proof):

        blockchain.new_transaction('0', values['id'], 1)

        #forge new block by adding ...the proof
        previous_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.new_block(proof, previous_hash)
    else:
        response={
            'message': 'Proof was invalid or late'
        }
        return jsonify(response), 200

    # Run the proof of work algorithm to get the next proof
    proof = blockchain.proof_of_work(blockchain.last_block)
    # Forge the new Block by adding it to the chain with the proof
    previous_hash = blockchain.hash(blockchain.last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'new_block': block
    } #dictionary for response because similar keys:values data structure

    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'message': 'hello'
        'chain': blockchain.chain,
        'length': len(blockchain.chain)'
    }
    return jsonify(response), 200

# Add an endpoint called `last_block` that returns the last block in the chain
@app.route('/last_block', methods=['GET'])
def return_last_block():
    response = {
        'last_block': blockchain.last_block
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def recieve_transactions():
    values = request.get_json()
    #breakpoint()
    required=['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        response = {'message': 'Missing values'}
        return jsonify(response), 400
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {
        'message': f'Transaction will be added to block{amount}.'
    }
    return jsonify(response), 201

# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
