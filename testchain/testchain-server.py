from flask import Flask
from flask import request
from ressources.blocks import Block

import json
import requests
import datetime as date

node = FLASK(__name__)

# Generate genesis block
def create_genesis_block():
    # Manually construct the genesis block
    return Block(0,date.datetime.now(),{
        "proof-of-work": 9,
        "transactions": None
        }, "0")

# A completely random address of the owner of this node
miner_address = "7xnh37inc7reyopc4rvik8kqfvd7g3se"
# Initialize this nodes copy of the blockchain
blockchain = []
blockchain.append(create_genesis_block())
# Store the transactions of this node
this_nodes_transaction = []
# Store the url data of every other node in the network so that we can communicate with them
peer_nodes = []
# are we mining or not?
mining = True

@node.route('/txion', methods=['POST'])
def transaction():
    # on each new POST request, we extract the transaction data
    new_txion = request.get_json()
    this_nodes_transactions.append(new_txion)
    print("New transaction")
    print("FROM: " + new_txion['from'].encode('ascii','replace'))
    print("TO: " + new_txion['to'].encode('ascii','replace'))
    print("AMOUNT: " + new_txion['amount'])
    # let the client know the transaction was successful
    return "Transaction successful\n"

@node.route('/blocks', methods=['GET'])
        def get_blocks():

def find_new_chains():
    # get the chains of every other node
    other_chains = []
    for node_url in peer_nodes:
        block = requests.get(node_url + "/blocks").content
        block = json.loads(block)
        other_chains.append(block)
    return other_chains

def consensus():
    # get the block from the other nodes
    other_chains = find_new_chains()
    # longest chain rule, if ours isn't the longest, then we store the longest chain
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    blockchain = longest_chain

def proof_of_work(last_proof):


