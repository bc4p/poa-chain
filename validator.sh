pk=$1
pw=$2
bn=$3
port=$4
netid=$5

geth init --datadir data genesis.json

geth --datadir data \
  --networkid "$netid" \
  --unlock "$pk" \
  --password "$pw" \
  --bootnodes "$bn" \
  --mine \
  --syncmode=full \
  --port "$port"
