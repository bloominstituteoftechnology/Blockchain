import hashlib
import requests

import sys
import json


#server only alidates a proof
#minor does all the work so minor has to have proof of work function s


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    # TODO
    #get block and turn it into string
    #The block dictionary needs to be a string before it can be hashed. This just turns the dictionary into a string. block_string and proof are then used to create the guess_hash
    block_string = json.dumps(block, sort_keys=True)
    proof = 0 

    while valid_proof(block_string, proof) is False:
        proof +=1
    # return proof
    return proof



def valid_proof(block_string, proof):
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
    #encode returns encoded version of given string
    #strings are stored as unicode (each character represnted by a code point) - so each string is a sequence of unicode points
    #for efficient storage of these strings, sequeunce of code points are converted ito set of bytes - this process is known as ENCODING
    #by default, encode uses utf-8 for default 

    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    #always returns false unless first 6 characters of hash are 0s
    return guess_hash[:6] == "000000"



if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"


 

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    coins_mined  = 0
    # Run forever until interrupted
    while True:
        #Get the last block from the server
        #does this work? 
        r = requests.get(url=node + "/last_block")
        # print('here is the last block r', r)
        # Handle non-json response
        
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break
       
        print(f"\nStarting mining ")
        # TODO: Get the block from `data` and use it to look for a new proof
        
        # Get lask block and that proof

        block = data['last-block']

        #find our prooof of that
        new_proof = proof_of_work(block)
        
        print(f'Proof found: {new_proof}')

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        #mine a coin 
        r = requests.post(url=node + "/mine", json=post_data)

        try: 
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break


        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        print(data['message'])
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data['message'])

