from web3 import Web3
import random
import json


rpc_url = "https://eth-mainnet.alchemyapi.io/v2/7R8FD0Z9VuycQYgASfO5xsfAPsK21DJW"
w3 = Web3(Web3.HTTPProvider(rpc_url))

if w3.is_connected():
    pass
else:
    print("Failed to connect to Ethereum node!")


def is_ordered_block(block_num):
    block = w3.eth.get_block(block_num)
    ordered = False
    transactions = [w3.eth.get_transaction(tx_hash) for tx_hash in block.transactions]
    if block_num <= 12965000:  # Pre-London Hard Fork
        ordered = all(
            tx.gasPrice >= transactions[i + 1].gasPrice
            for i, tx in enumerate(transactions[:-1])
        )
    else:  # Post-London Hard Fork (EIP-1559)
        ordered = all(
            (
                (
                    tx.maxPriorityFeePerGas + block.baseFeePerGas
                )
                <= (
                    transactions[i + 1].maxPriorityFeePerGas +
                    block.baseFeePerGas
                )
                if tx.type == 2 and transactions[i + 1].type == 2
                else tx.gasPrice >= transactions[i + 1].gasPrice
            )
            for i, tx in enumerate(transactions[:-1])
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
