import hashlib
import requests
import sys
import json
def proof_of_work():
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    # block_string = json.dumps(block, sort_keys=True)
    proof = 32166570
    while valid_proof(proof) is False:
        proof += 1
    # guess = f'{block_string}{proof}'.encode()
    # guess_hash = hashlib.sha256(guess).hexdigest()
    # print(guess)
    # print(guess_hash)
    return print(proof)
def valid_proof(proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    # proof here is like salt, block string is the same salt in this case is changing until we find correct hash
    guess = f'{19647468}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"
    
while True:
    proof_of_work()