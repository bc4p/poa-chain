docker compose stop $1
docker compose rm -f $1
sudo rm -rf data/$1
docker compose up -d $1
