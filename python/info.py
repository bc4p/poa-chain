from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

latest = w3.eth.get_block('latest')

print(w3.eth.block_number)

print(latest)

addresses = [
    '0x2d558F4633FF8011C27401c0070Fd1E981770B94', '0x71f9BE88bE65aaa703918b0a09f84D4b015A1bc8',
    '0x66DFE79b64F64718430ffc468806FB3E13853651', '0x388C9150daea7e36560c6A22A88D6fE7d3749845'
]

for address in addresses:
    print(address, w3.eth.get_balance(address))
