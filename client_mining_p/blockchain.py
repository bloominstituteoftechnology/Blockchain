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

        # Create the genesis block
        # created different since it has no previous block to pull data for the proof
        self.new_block(previous_hash=1, proof=100)

    def new_transaction(self, sender, recipient, amount):
        """ 
        creates a new transaction to go into the next mined block


        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index']+1

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
            'proof':  proof,
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
        # sort_keys = True will allow the dict to be ordered the same way each time.... big deal for this usage
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

    # MOVE TODO - remove this from the server and setup on the client side.
    # def proof_of_work(self, block):
    #     """
    #     Simple Proof of Work Algorithm
    #     Stringify the block and look for a proof.
    #     Loop through possibilities, checking each one against `valid_proof`
    #     in an effort to find a number that is a valid proof
    #     :return: A valid proof for the provided block
    #     """
    #     block_string = json.dumps(block, sort_keys=True)

    #     proof = 0

    #     while self.valid_proof(block_string, proof) == False:
    #         proof += 1

    #     return proof
    # # VP TODO - change to have 6 zeros at teh start below instead of 3
    # will need to change the slice to check for it also and the string to '000000'
    # maybe wait to change this after all else is working to be faster in testing it out
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
        print(f"is {proof} valid?")
        guess = block_string + str(proof)
        guess = guess.encode()

        hash_value = hashlib.sha256(guess).hexdigest()
        print(hash_value)

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
        'text': 'hello World'
    }
    return jsonify(response), 200

# Mine TODO - this is where it says to modify to instead recieve and validate or reject a new proof sent from client(miner)
# it should accept a post
# use 'data = request.get_json()' to pull the data out of the post
# note that request and requests are both in this project
# check that proof and id are present
# return with 400 error using jsonify(response) with a message
# return message indicating success or failure
# valid proof should fail for all senders except the first
# @app.route('/mine', methods=['GET'])
# def mine_get():
#    # Run the proof of work algorithm to get the next proof'

#     print("we shall now mine a block!")

#     proof = blockchain.proof_of_work(blockchain.last_block)

#     print(f"after a long process... here it is... {proof}")

#     # Forge the new Block by adding it to the chain with the proof

#     new_block = blockchain.new_block(proof)

#     response = {
#         'block': new_block,
#     }

#     return jsonify(response), 200


@app.route('/mine', methods=['POST'])
def mine_post():
    # print(f'we have a post')
    data = request.get_json()
    if 'id' not in data or 'proof' not in data:
        response = {'message': "missing data"}
        return jsonify(response), 400
    print("data from request:", data)
    # print('that was the data above...... does this print?')
    proof = data['proof']
    print(proof)
    p_id = data['id']
    print(p_id)

    last_block = blockchain.last_block
    block_string = json.dumps(last_block, sort_keys=True)

    if blockchain.valid_proof(block_string, proof):
        # lets mine a new block and return success
        blockchain.new_transaction(
            sender="0",
            recipient=data['id'],
            amount=1
        )
        new_block = blockchain.new_block(proof)

        response = {
            'block': new_block,
            'made_by': p_id,
        }
        print(response)
        return jsonify(response), 200

    else:
        # respond with error message
        response = {
            'message': "invalid proof!"
        }
        return jsonify(response), 400


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'len': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200

# DONE add the endpoint call 'last_block' to return the last block in the chain
@app.route('/last_block', methods=['GET'])
def last_block():

    last = blockchain.last_block

    response = {
        'last_block': last
    }
    return jsonify(response), 200


@app.route('/transactions_new', methods=['POST'])
def new_transactions():
    data = request.get_json()

    # check that require fields are present
    if 'recipient' not in data or 'amount' not in data or 'sender' not in data:
        response = {'message': "Error: missing values"}
        return jsonify(response), 400

    index = blockchain.new_transaction(
        data['sender'], data['recipient'], data['amount'])
    response = {
        'message': f'transaction will be posted in block with index {index}'
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
