# Create docker network
docker network inspect testnet >/dev/null 2>&1 || docker network create testnet
docker network inspect testnet >/dev/null 2>&1 || docker network create testnet

# update ts repos needed
rm -rf ts_standardscripts
rm -rf ts_externalscripts
git clone --depth 1 https://github.com/lsst-ts/ts_standardscripts.git
git clone --depth 1 https://github.com/lsst-ts/ts_externalscripts.git

# update and restart the LOVE
docker-compose pull
docker-compose down -v
source local_env.sh; docker-compose up -d