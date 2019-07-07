import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request
from urllib.parse import urlparse
import requests

import sys


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.genesis_block()

        # Don't create a block automatically.  If we do,
        # every node will have a different anchor
        # self.new_block(previous_hash=1, proof=99)  # 99 is faster for 1st

    def genesis_block(self):
        """
        Create the genesis block and add it to the chain

        The genesis block is the anchor of the chain.  It must be the
        same for all nodes, or their chains will fail consensus.

        It is normally hard-coded
        """
        block = {
            'index': 1,
            'timestamp': 0,
            'transactions': [],
            'proof': 99,  # 99 is faster for 1st proof gen
            'previous_hash': 1,
        }

        self.chain.append(block)

    def new_block(self, proof, previous_hash):
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
            'previous_hash': previous_hash,
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def add_block(self, block):
        """
        Add a received Block to the end of the Blockchain

        :param block: <Block> The validated Block sent by another node in the
        network
        """

        # Reset the current list of transactions.  TODO: Handle pending
        # transactions
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

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm
        - Find a number p' such that hash(pp') contains 6 leading
        zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof:  Does hash(last_proof, proof) contain 6
        leading zeroes?
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:6] == "000000"

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
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than
        # ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def broadcast_new_block(self, block):
        """
        Alert neigbors in list of nodes that a new block has been mined
        :param block: <Block> the block that has been mined and added to the 
        chain
        """
        neighbours = self.nodes

        post_data = {"block": block}

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.post(f'http://{node}/block/new',
                                     json=post_data)

            if response.status_code != 200:
                # Error handling
                pass


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    # Determine if proof is valid
    last_block = blockchain.last_block
    last_proof = last_block['proof']

    values = request.get_json()
    submitted_proof = values.get('proof')

    if blockchain.valid_proof(last_proof, submitted_proof):
        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mine a new coin
        blockchain.new_transaction(
            sender="0",
            recipient=node_identifier,
            amount=1,
        )

        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        # print('Hash is: ' + str(previous_hash), file=sys.stderr)
        block = blockchain.new_block(submitted_proof, previous_hash)

        # Broadcast the new block
        blockchain.broadcast_new_block(block)

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
            'message': "Proof was invalid or already submitted."
        }
        return jsonify(response), 200


# Receive a new block from a peer
@app.route('/block/new', methods=['POST'])
def new_block():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['block']
    if not all(k in values for k in required):
        return 'Missing Values', 400

    # TODO: Verify that the sender is one of our peers

    # Check that the new block index is 1 higher than our last block
    new_block = values.get('block')
    old_block = blockchain.last_block
    print('new block received', file=sys.stderr)
    print('with index' + str(new_block.get('index: ')), file=sys.stderr)
    if new_block.get('index') == old_block.get('index') + 1:
        # Verify the block by making sure the previous hash matches
        print('and has the correct index', file=sys.stderr)
        if (new_block.get('previous_hash') ==
                blockchain.hash(blockchain.last_block)):
            print('new block accepted', file=sys.stderr)
            blockchain.add_block(new_block)
            return 'Block Accepted', 200
        else:
            return 'Invalid Block, hash does not match', 400
    # Otherwise, check for consensus
    else:
        # TODO: This locks both servers while they await a response
        # from the other server
        print('seeking consensus', file=sys.stderr)
        consensus()
        return 'Seeking consensus from network', 200


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
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/last_proof', methods=['GET'])
def last_proof():
    last_proof_value = blockchain.last_block.get('proof')
    response = {
        'proof': last_proof_value
    }
    return jsonify(response), 200


# Post body as JSON to add node
# {
# 	"nodes": ["http://localhost:5001"]
# }
@app.route('/nodes/register', methods=['POST'])
def register_nodes():

    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


# Note, when demoing, start with this, then change to the below
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5000
    app.run(host='0.0.0.0', port=port)
