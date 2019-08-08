import hashlib
import requests
import time
import sys

# TODO: Implement functionality to search for a proof


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"


    def invalid_proof(last_proof, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 6
        leading zeroes?
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        beg = guess_hash[:7]

        if beg == "0000000":
            return False
        else:
            return True

    coins_mined = 0
    proof = 0
    invalid = True
    last_proof = requests.get(node + "/last-proof")

    start = time.time()
    while invalid:
        invalid = invalid_proof(last_proof.content, proof)

        now = time.time()
        sys.stdout.write("\rValidating proof. {0} seconds elapsed.".format(now - start))
        sys.stdout.flush()

        if not invalid:
            coins_mined += 1
            response = requests.post(node + "/mine", data={'last_proof': last_proof.content, 'proof': proof})

            print(response.content.message)

        else:
            proof += 1

