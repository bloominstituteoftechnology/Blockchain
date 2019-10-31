# Paste your version of blockchain.py from the client_mining_p
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
        self.nodes = set()

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
            # TODO
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        # Append the chain to the block
        # Return the new block
        # pass
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append(
            {'sender': sender, 'recipient': recipient, 'amount': amount})
        return self.last_block['index'] + 1


    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It convertes the string to bytes.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        # TODO: Hash this string using sha256

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        # pass
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
        # TODO
        # pass
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:3] == "000"
        # return True or False

    

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    '''handle non json responses
    and check that the required fields are in the posted data
    '''
    data = request.get_json()
    print('====+++====', data.get('proof'))
    required_fields = ['proof', 'id']
    if not all(k in data for k in required_fields):
        return jsonify({
            'message': 'You need to pass in an Id and proof'
        }), 400

     # get the submitted proof from the values data
    submitted_proof = data.get('proof')
    last_block_string = json.dumps(
        blockchain.last_block, sort_keys=True).encode()

    proof_valididty = blockchain.valid_proof(
        last_block_string, submitted_proof)

    if proof_valididty:
        previous_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.new_block(submitted_proof, previous_hash)

        # reward miner for guessing proof
        blockchain.new_transaction(
            sender="0", recipient=node_identifier, amount=1)
        response = {
            # TODO: Send a JSON response with the new block
            'message': 'Newly Forged Block',
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }

        return jsonify(response), 200
    else:
        return jsonify({
            'message': 'invalid proof'
        }), 200

    # Run the proof of work algorithm to get the next proof
    # proof = blockchain.proof_of_work()
    # Forge the new Block by adding it to the chain with the proof
    # previous_hash = blockchain.hash(blockchain.last_block)
    # block = blockchain.new_block(proof, previous_hash)

    # response = {
    #     # TODO: Send a JSON response with the new block
    #     'message': 'Newly Forged Block',
    #     'index': block['index'],
    #     'transactions': block['transactions'],
    #     'proof': block['proof'],
    #     'previous_hash': block['previous_hash'],
    # }

    # return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'length': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def last_block():
    response = {
        'length of blockchain': len(blockchain.chain),
        'last_block': blockchain.last_block
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # get the values in json format
    data = request.get_json()
    # check that the required fields exist
    required_fields = ['sender', 'recipient', 'amount']

    if not all(k in data for k in required_fields):
        return jsonify({
            'message': 'You need to pass in all required fields'
        }), 400

    # create a new transaction
    index = blockchain.new_transaction(
        data['sender'], data['recipient'], data['amount'])

    # set the response object with a message that the transaction will be added at the index
    response = {'message': f'Transaction will be added to Block {index}'}
    # return the response
    return jsonify(response), 201


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
