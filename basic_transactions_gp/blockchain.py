import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
from flask_cors import CORS


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Create the genesis block
        self.new_block(proof=100, previous_hash=1)

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

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append(
            {'sender': sender, 'recipient': recipient, 'amount': amount})
        return self.last_block['index'] + 1

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
        # It convertes the string to bytes.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes
        # TODO: Create the block_string
        # stringify's the "block" into 1 string, and sorts the keys in an "order"
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()  # changes string to "byte-like" object
        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()
        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand
        # TODO: Return the hashed block string in hexadecimal format
        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]
    # def proof_of_work(self, block):
    #     """
    #     Simple Proof of Work Algorithm
    #     Stringify the block and look for a proof.
    #     Loop through possibilities, checking each one against `valid_proof`
    #     in an effort to find a number that is a valid proof
    #     :return: A valid proof for the provided block
    #     """
    #     # Proof is a SHA256 hash with 3 leading zeroes
    #     block_string = json.dumps(block, sort_keys=True).encode()
    #     proof = 0
    #     while not self.valid_proof(block_string, proof):
    #         proof += 1
    #     guess = f'{block_string}{proof}'.encode()
    #     guess_hash = hashlib.sha256(guess).hexdigest()
    #     return proof, guess_hash
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
        # "01234""5" => "012345"
        # "blockstring""proof" => "blockstring100"
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()  # "0000678"
        # return True or False
        return guess_hash[:5] == "00000"


# Instantiate our Node
app = Flask(__name__)
CORS(app)
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
# Instantiate the Blockchain
blockchain = Blockchain()
@app.route('/mine', methods=['POST'])
def mine():
    # Run the proof of work algorithm to get the next proof
    # proof, previous_hash = blockchain.proof_of_work(blockchain.last_block)
    # Forge the new Block by adding it to the chain with the proof
    # previous_hash = blockchain.hash(blockchain.last_block)
    # block = blockchain.new_block(proof, previous_hash)
    last_block = blockchain.last_block
    last_block_string = json.dumps(last_block, sort_keys=True).encode()
    try:
        data = request.get_json()
        post_proof = data["proof"]
        post_id = data["id"]
    except KeyError:
        return jsonify({"message": "You need to pass in proof or id"}), 400
    if blockchain.valid_proof(last_block_string, post_proof):
        proof = f'{last_block_string}{post_proof}'.encode()
        proof_hash = hashlib.sha256(proof).hexdigest()
        blockchain.new_transaction(sender="0", recipient=post_id, amount=1)
        new_block = blockchain.new_block(post_proof, proof_hash)

        return jsonify({'message': 'New Block Forged'}), 200
    else:
        return jsonify({
            "message": "Error"
        }), 404


@app.route('/last_block', methods=['GET'])
def get_last_block():
    response = {
        "last_block": blockchain.last_block
    }
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'length': len(blockchain.chain),
        'chain': blockchain.chain,
    }
    return jsonify(response), 200


@app.route('/', methods=['GET'])
def home():
    return "<h1>HELLO</h1>", 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
