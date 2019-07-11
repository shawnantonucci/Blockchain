import hashlib
import requests
import json

from flask import Flask, jsonify, request

import sys


# TODO: Implement functionality to search for a proof

def proof_of_work():
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 4 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """

    print("Searching for proof")
    response = requests.get('http://localhost:5000/last_proof')
    json_string = json.dumps(response)
    print("last_proof: ", json_string)

    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    return proof

def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 4
    leading zeroes?
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # return guess_hash[:6] == "000000"
    # print(guess_hash, "guess hash")
    # print("last_proof: ", last_proof)
    data = json.dumps({"data": guess_hash, "last_proof": last_proof})
    # print("data: ", guess_hash)
    valid_proof = requests.post('http://localhost:5000/mine', data = data)
    print("Valid proof: ", valid_proof.data)

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"


    coins_mined = 0
    # Run forever until interrupted
    run_once = True
    # while True:
    while run_once:
        proof_of_work()
        # TODO: Get the last proof from the server and look for a new one
        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        run_once = False
        pass
