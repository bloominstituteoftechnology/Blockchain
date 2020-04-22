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
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.last_block)
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
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
        block_string = json.dumps(block, sort_keys=True)

        # TODO: Hash this string using sha256
        # first convert to a byte string

        hashed_block = hashlib.sha256(block_string.encode())

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return hashed_block.hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route("/", methods=['GET'])
def greet():
    response = {
        "greeting": "Hello, World!"
    }

    return jsonify(response), 200


@app.route('/mine', methods=['POST'])
def mine():
    # just like getting request body
    data = request.get_json()

    if "id" not in data or "proof" not in data:
        response = {"message": "missing data"}
        return jsonify(response), 400

    # Run the proof of work algorithm to get the next proof
    proof = data["proof"]
    last_block = blockchain.last_block
    block_string = json.dumps(last_block, sort_keys=True)

    if blockchain.valid_proof(block_string, proof):
        # return a the new block
        new_block = blockchain.new_block(proof)
        response = {
            "block": new_block
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "invalid proof"
        }

    # Forge the new Block by adding it to the chain with the proof
    new_block = blockchain.new_block(proof)

    response = {
        "block": new_block
    }

    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def last_block():
    pass


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        "len": len(blockchain.chain),
        "chain": blockchain.chain
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
