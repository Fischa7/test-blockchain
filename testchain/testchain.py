from ressources.blocks import Block
import datetime as date

def create_genesis_block():
    # Manually construct a block with 
    # index zero and arbitrary previous hash
    return Block(0, date.datetime.now(), "Genesis Block", "0")

def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "Hey! I'm block " + str(this_index)
    this_hash = last_block.hash
    block = Block(this_index, this_timestamp, this_data, this_hash)
    return block

# Create the blockchain and add the genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# This indicates how many blocks should be added to the chain after genesis
num_of_blocks_to_add = 20

# Add the blocks to the blockchain
for i in range(num_of_blocks_to_add):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add

    # Let the world know
    print("Block #" +str(block_to_add.index) + " has been added to the blockchain!")
    print("Hash: {" + str(block_to_add.hash) + "}\n")
