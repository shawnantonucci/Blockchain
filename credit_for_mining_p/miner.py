import hashlib
import requests
from uuid import uuid4

import os.path
from os import path

import sys


def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 6 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """

    print("Searching for next proof")
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    print("Proof found: " + str(proof))
    return proof


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 6
    leading zeroes?
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"

def get_client_id():
    # check for id in file
    exists = path.exists("my_id.txt")
    client_ID = ''
    if exists:
        # check if file contains anything on line1
            id_file = open('./my_id.txt', 'r+')
            string = id_file.read()
            if len(string) > 0:
                client_ID = string
            id_file.close()


    if len(client_ID) == 0:
        client_ID = str(uuid4()).replace('-', '')
        print("Client ID: ", client_ID)
        # add unique ID to text file
        id_file = open('./my_id.txt', 'a')
        id_file.write(client_ID)
        id_file.close()

    return client_ID


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = int(sys.argv[1])
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        client_ID = get_client_id()
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        # TODO: add unique ID to post_data
        post_data = {"proof": new_proof, "client_ID": client_ID}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
