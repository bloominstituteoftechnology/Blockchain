import hashlib
import requests
import sys
import json

#we want other people to do the mining and we reward them for doing it

def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    pass

    #block is passed to json.dumps to be converted into a string before being encoded and
    #passed to hashlib.sha256
    block_string = json.dumps(block, sort_keys=True)

    #nonce value combined with the contents of the block in valid_proof to generate the guess hash
    #we don't have to encode the proof since we are combining it with another string
    #a way to do this is to guess, start at 0 and start guessing numbers
    proof = 0

    #this will run until it finds one that works
    while valid_proof(block_string, proof) is False:
        #increments the proof value until the hash with the required difficulty has been generated.
        proof += 1

    #after we find one that works, we return proof
    return proof


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
        #encode the block_string and proof (nonce value) passed in from proof_of_work
        guess = f'{block_string}{proof}'.encode()

        #hashes and converts guess to hexadecimal format (readable format that we can compare)
        guess_hash = hashlib.sha256(guess).hexdigest()

        #return guess_hash if it contains 6 leading zeros
        return guess_hash[:6] == "000000"



if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    # you can provide an endpoint on the command line when python "name_of_file.py" is entered
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        #or use node + "end point name"in requests.get and requests.post
        node = "http://localhost:5000"

    # Load ID
    #open text file and read id
    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    #Add any coins granted to a simple integer total, and print the amount of coins the client has earned
    total_coins = 0

    # Run forever until interrupted
    # Continue mining until the app is interrupted.
    while True:
        #Print messages indicating that this has started and finished.
        print("mining started")

        # Get the last block from the server
        # by visiting the endpoint that is in node + last_block 
        r = requests.get(url=node + "/last_block")

        # Handle non-json response
        try:
            #use .json to get the json encoded content of a response
            #encode the results of sending a get request to the last_block endpoint
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: Get the block from `data` and use it to look for a new proof
        #a block object called last_block with index, previous_hash, proof, timestamp, transactions is 
        # returned from get endpoint
        last_block = data['last_block']
        print(f'Last Block: {last_block}')

        # new_proof = ???
        #send the last block retrieved from the last_block endpoint to proof_of_work method
        new_proof = proof_of_work(last_block)

        #if proof_of_work returns a valid proof 
        print(f'Proof found: {new_proof}')

        #breakpoint() used to pause the program to examine what data it contains 

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        #post the data object with proof and id to the mine endpoint and store the response in r
        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        #use .json to get the json encoded content of the response from the server
        # data = r.json()

         # Handle non-json response
        try:
            #use .json to get the json encoded content of a response
            #encode the results of sending a get request to the last_block endpoint
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break


        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        pass
        # print the error message "Invalid or already submitted proof"
        if data['message'] == 'New Block Forged':            

           total_coins = total_coins + 1
           print(f'Number of coins mined: {total_coins}')
        else:            
            print(data['message'])

        #Print messages indicating that this has started and finished.
        print("mining ended")    