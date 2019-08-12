import hashlib
import json
from time import time
from uuid import uuid4
from urllib.parse import urlparse
import sys

from flask import Flask, jsonify, request, redirect, url_for, flash, render_template

# driver = webdriver.Firefox()

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        self.gensis_block()

    def genesis_block(self):
        block = {
            'index': 1,
            'timestamp': 0,
            'transactions': [],
            'proof': 99,
            'previous_hash': 1,
        }

        self.chain.append(block)


    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

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

        self.chain.append(block)
        return block

    def add_block(self,block):
        self.current_transactions = []
        self.chain.append(block)

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
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_block_string):
        proof = 0

        while self.valid_proof(blockchain.last_block['previous_hash'], proof) is False:

            proof += 1

        return proof



    @staticmethod
    def valid_proof(last_block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 6
        leading zeroes?
        """
        #String to hash
        guess = f'{last_block_string}{proof}'.encode()
        #Hash string
        guess_hash = hashlib.sha256(guess).hexdigest()
        #check for 6 leading 0s
        beg = guess_hash[:6]
        return beg == '000000'

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-------------------\n")
            if block['previous_has'] != self.hash(last_block):
                return False
            last_block = block
            current_index += 1

        return True

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.nettloc)
    
    def resolve_conflicts(self):
        neighbors = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbors:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True
        
        return False


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()



@app.route('/mine', methods=['POST'])
def mine():
    last_block = blockchain.last_block

    last_block_string = last_block['previous_hash']


    
    values = request.get_json()
    submitted_proof = values.get('proof')

    required = ['proof']
    if not all(k in values for k in required):
        return 'Missing Values', 400


    if blockchain.valid_proof(last_block_string, submitted_proof):

        blockchain.new_transaction(
            sender='0',
            recipient=node_identifier,
            amount=1,
        )

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
        response = {
            'message': 'Proof was invalid or already submitted'
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
        # TODO: Return the chain and its current length
        'currentChain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/last_block_string', methods=['GET'])
def last_block_string():

    last_block = blockchain.last_block
    last_block_string = last_block['proof']

    response = {
        # TODO: Return the chain and its current length
        'last_block_string': blockchain.last_block

    }
    return jsonify(response), 200


# Run the program on port 5000
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5000
    app.run(host='0.0.0.0', port=port)