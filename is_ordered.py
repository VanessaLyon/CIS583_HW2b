from web3 import Web3
import random
import json

rpc_url = "https://eth-mainnet.alchemyapi.io/v2/7R8FD0Z9VuycQYgASfO5xsfAPsK21DJW"
w3 = Web3(Web3.HTTPProvider(rpc_url))

if w3.is_connected():
	pass
else:
	print( "Failed to connect to Ethereum node!" )

"""
	Takes a block number
	Returns a boolean that tells whether all the transactions in the block are ordered by priority fee

	Before EIP-1559, a block is ordered if and only if all transactions are sorted in decreasing order of the gasPrice field

	After EIP-1559, there are two types of transactions
		*Type 0* The priority fee is tx.gasPrice - block.baseFeePerGas
		*Type 2* The priority fee is min( tx.maxPriorityFeePerGas, tx.maxFeePerGas - block.baseFeePerGas )

	Conveniently, most type 2 transactions set the gasPrice field to be min( tx.maxPriorityFeePerGas + block.baseFeePerGas, tx.maxFeePerGas )
"""

def is_ordered_block2(block_num):
    block = w3.eth.get_block(block_num)
    ordered = False

    if block_num <= 12965000:  # Pre-London Hard Fork
        ordered = all(
            (
                (tx.gas_price if isinstance(tx, str) else tx.gas_price)
                >=
                (tx2.gas_price if isinstance(tx2, str) else tx2.gas_price)
            )
            for tx, tx2 in zip(block.transactions[:-1], block.transactions[1:])
        )
    else:  # Post-London Hard Fork (EIP-1559)
        ordered = all(
            (
                (
                    (
                        (tx.get("type") == 2 and tx2.get("type") == 2 and
                         tx.get("max_priority_fee_per_gas", 0) + block.base_fee_per_gas <=
                         tx2.get("max_priority_fee_per_gas", 0) + block.base_fee_per_gas)
                    )
                    if isinstance(tx, dict) and isinstance(tx2, dict)
                    else (tx.gas_price if isinstance(tx, str) else tx.gas_price) >=
                         (tx2.gas_price if isinstance(tx2, str) else tx2.gas_price)
                )
            )
            for tx, tx2 in zip(block.transactions[:-1], block.transactions[1:])
        )

    return ordered

def is_ordered_block(block_num):
    block = w3.eth.get_block(block_num)
    ordered = False

    if block.transactions:
        ordered = all(
            block.transactions[i]["gas_price"] >= block.transactions[i + 1]["gas_price"]
            for i in range(len(block.transactions) - 1)
        )

    return ordered


"""
	This might be useful for testing
"""
if __name__ == "__main__":
	latest_block = w3.eth.get_block_number()

	london_hard_fork_block_num = 12965000
	assert latest_block > london_hard_fork_block_num, f"Error: the chain never got past the London Hard Fork"

	n = 5

	for _ in range(n):
        #Pre-London
		block_num = random.randint(1,london_hard_fork_block_num-1)
		ordered = is_ordered_block(block_num)
		if ordered:
			print( f"Block {block_num} is ordered" )
		else:
			print( f"Block {block_num} is ordered" )

        #Post-London
		block_num = random.randint(london_hard_fork_block_num,latest_block)
		ordered = is_ordered_block(block_num)
		if ordered:
			print( f"Block {block_num} is ordered" )
		else:
			print( f"Block {block_num} is ordered" )

