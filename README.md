# poa-chain
Docker-Compose configuration to start a PoA chain with 3 Validators


## Setup
This Setup consists of  3 Validators, a bootnode and a node which offers APIs for Interaction with the chain.

### Prefunded Accounts of the Validators

- Publickey 1: 
```
e3a6375595003104ea6edcf0543a583118a5dd2b
```
- Publickey 2: 
```
893356c8b396bd36dbd32ff754e811ff95978e24
```
- Publickey 3: 
```
70c0fadde839bd08fe0d9058972cb76be4130810
```
### Change defaults

Create your own Bootnode Credentials:
```
docker-compose exec tools sh
bootnode -genkey newbootnode.key
```

Create your own Validator Credentials
```
docker-compose exec tools sh
geth account new --datadir data
```

The keystore file under /data/keystore contains the private key.

### After first start

Add a second validator:
```
docker compose exec validator1 geth attach --exec 'clique.propose("0x66DFE79b64F64718430ffc468806FB3E13853651", true)' /data/geth.ipc 
```

Add the third validator:
```
docker compose exec validator1 geth attach --exec 'clique.propose("0x388C9150daea7e36560c6A22A88D6fE7d3749845", true)' /data/geth.ipc
docker compose exec validator2 geth attach --exec 'clique.propose("0x388C9150daea7e36560c6A22A88D6fE7d3749845", true)' /data/geth.ipc
```

Check success via:
```
docker compose exec node geth attach --exec 'clique.status()' /data/geth.ipc
docker compose exec node geth attach --exec 'clique.getSigners()'/ /data/geth.ipc 
```
Sent test transaction
```
docker compose exec validator1 geth attach --exec 'eth.sendTransaction({from: "0x2d558F4633FF8011C27401c0070Fd1E981770B94",to: "0x71f9BE88bE65aaa703918b0a09f84D4b015A1bc8", value: "5000000000000000000"})' /data/geth.ipc 
```

## Connect via Metamask

Install Metamask as Browser add-on https://metamask.io/ and add a new Network with the following details:


- Network Name: Free to choose (BC4P Net)
- RPC-URL: https://bc4p.nowum.fh-aachen.de/blockchain
- ChainID: 123321
- Symbol: Free to choose (BC4P)
- Block-Explorer: https://bc4p.nowum.fh-aachen.de/explorer
- Hit save

You should now be able to receive and send BC4P Tokens via your Public Address, which u can find at the top in Metamask it should look something like this: 
```
0xab2c78a84A838073b26601da041b27ceB4682d17
```

## Faucet or How to get my first BC4P Tokens

- Ask someone who already has Tokens to send u some.
- Use the Faucet under https://bc4p.nowum.fh-aachen.de/faucet and enter your Public Address to receive some BC4P Tokens.


## Connect via web3

A method to connect via Python and the Web3 modul. You can find more examples in the Python directory of this repository

```
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://bc4p.nowum.fh-aachen.de/blockchain'))
```

