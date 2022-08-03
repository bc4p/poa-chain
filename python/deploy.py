import time

from web3 import Web3
from web3.middleware import geth_poa_middleware

from data import abi, bytecode, private_key

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract_ = w3.eth.contract(
    abi=abi,
    bytecode=bytecode,
)

local_acc = w3.eth.account.privateKeyToAccount(private_key)

construct_txn = contract_.constructor().buildTransaction({
    'from': local_acc.address,
    'nonce': w3.eth.getTransactionCount(local_acc.address),
    'gas': 4700000,
    'gasPrice': w3.toWei('21', 'gwei'),
})

signed_tx = local_acc.signTransaction(construct_txn)
tx = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(tx.hex())

time.sleep(10)

receipt = w3.eth.get_transaction_receipt(tx)
print(receipt)

with open('contract.txt', 'w') as the_file:
    the_file.write(receipt['contractAddress'])
