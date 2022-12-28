bn=$1
port=$2
netid=$3
geth init --datadir data genesis.json

geth --datadir data \
  --http --http.addr '0.0.0.0' --http.port 8545 --http.corsdomain '*' \
  --http.api 'admin,debug,web3,eth,txpool,personal,clique,miner,net,txpool ' \
  --networkid "$netid" \
  --bootnodes "$bn" \
  --syncmode=full \
  --http.vhosts '*' \
  --gcmode="archive" \
  --port "$port"

#  --nat extip 10.13.10.61
