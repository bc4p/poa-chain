import random

from web3 import Web3
from web3.middleware import geth_poa_middleware

from data import abi, private_key

with open('contract.txt', 'r') as content_file:
    contract_address = content_file.read()

print("Contract address", contract_address)

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract_ = w3.eth.contract(address=contract_address, abi=abi)

local_acc = w3.eth.account.privateKeyToAccount(private_key)

current_value = contract_.functions.retrieve().call()
print(current_value)

new_value = random.randrange(1, 10000)
print(new_value)

put_tx = contract_.functions.store(new_value).buildTransaction({
    'from': local_acc.address,
    # 'to': contract_address,
    'nonce': w3.eth.getTransactionCount(local_acc.address),
    'gas': 50000,
    'gasPrice': w3.toWei('21', 'gwei'),
})

signed_tx = local_acc.signTransaction(put_tx)
tx = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(tx.hex())
