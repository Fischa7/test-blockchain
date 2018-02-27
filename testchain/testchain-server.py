from flask import Flask
from flask import request
from ressources.blocks import Block

import json
import requests
import datetime as date

node = Flask(__name__)

# Generate genesis block
def create_genesis_block():
    # Manually construct the genesis block
    return Block(0,date.datetime.now(),{
        "proof-of-work": 7,
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
    chain_to_send = blockchain
    blocklist = ""
    for i in range(len(chain_to_send)):
        block = chain_to_send[i]
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        assembled = json.dumps({
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "hash": block_hash
            })
        if blocklist == "":
            blocklist = assembled
        else:
            blocklist += assembled
    return blocklist

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
    # simplified proof of work, number needs to be divisible by 7 and the pow of the previous block
    inc = last_proof + 1
    while not (inc % 7 == 0 and inc % last_proof == 0):
        inc += 1
    # once the number is found, we can return it as pow
    return inc

@node.route('/mine', methods = ['GET'])
def mine():
    last_block = blockchain[len(blockchain) -1]
    last_proof = last_block.data['proof-of-work']
    # find the proof of work for current block being mined
    proof = proof_of_work(last_proof)
    # once valid pow is found, we reward the miner by adding a transaction
    this_nodes_transactions.append(
            {"from": "network", "to": miner_address, "amount": 1}
            )
    # now gather data to create new block
    new_block_data = {
            "proof-of-work": proof,
            "transactions": list(this_nodes_transactions)
            }
    new_block_index = last_block.index + 1 
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    # empty transaction list
    this_nodes_transactions[:] = []
    # now create the new block
    mined_block = Block(
            new_block_index,
            new_block_timestamp,
            new_block_data,
            last_block_hash)
    blockchain.append(mined_block)

    # let the client know, the block has been mined
    return json.dumps({
        "index": new_block_index,
        "timestamp": str(new_block_timestamp),
        "data": new_block_data,
        "hash": last_block_hash
    })

    node.run()
