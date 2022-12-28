#!/bin/sh

# to remove only stuck validators
# Unclean shutdown detected
# weird logs like "needed geth db freezer-migrate", but freezer migrate did not help
# geth rewinding blockchain
sudo rm -r data/validator1/geth
sudo rm -r data/validator2/geth #/chaindata
sudo rm -r data/validator3/geth #/chaindata
# they are pulling data from the node, which has access to the bc history
docker compose up -d

# to delete everything and start new
#sudo rm ./data/node/* data/validator1/* data/validator2/* data/validator3/* -r
