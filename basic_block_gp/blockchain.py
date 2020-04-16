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

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: <str> Address of the Recipient
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the BLock that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1


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
            'previous_hash': previous_hash or self.hash(self.last_block),
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
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256(block_string)

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand
        hash_string = raw_hash.hexdigest()
        # TODO: Return the hashed block string in hexadecimal format
        return hash_string

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
        # print(f"i will now check if {proof} is valid")
        guess = block_string + str(proof) 
        guess = guess.encode()

        hash_value = hashlib.sha256(guess).hexdigest()

        return hash_value[:3] == '000'


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/', methods=['GET'])
def hello_world():
    response = {
        'text': 'hello world'
    }
    return jsonify(response), 200

@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()
    if 'id' not in data or 'proof' not in data:
        response = {'message': 'missing values'}
        return jsonify(response), 400
    # Run the proof of work algorithm to get the next proof
    # print("We shall now mine a block!")
    proof = data['proof']
    last_block = blockchain.last_block 
    block_string = json.dumps(last_block, sort_keys=True)

    if blockchain.valid_proof(block_string, proof):
        # lets mine a new block, and return a success!    
        blockchain.new_transaction(
            sender="0",
            recipient=data['id'],
            amount=1
        )
        new_block = blockchain.new_block(proof)
        response = {
            'block': new_block
        }
        return jsonify(response), 200
    else:
        # respond with an error message
        response = {
            'message': 'Proof is invalid'
        }
        return jsonify(response), 200

@app.route('/last_block', methods=['GET'])
def return_last_block():
    response = {
        'last_block': blockchain.last_block
    }
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'len': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    data = request.get_json()

    # check that required fields are present
    if 'recipient' not in data or 'amount' not in data or 'sender' not in data:
        response = {'message' : 'Error: missing values'}
        return jsonify(response), 400
    
    # in the real world, we would probably want to verify that this transaction is legit
    # for now, we can allow anyone to add whatever they want

    # create the new transaction
    index = blockchain.new_transaction(data['sender'], data['recipient'], data['amount'])
    response = {'message': f'Transaction will be posted in block with index {index}'}
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
