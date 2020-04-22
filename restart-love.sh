#!/bin/sh
 
cwd=$(pwd)
current_time=$(date "+%Y.%m.%d-%H.%M.%S")
file_name=$cwd/love-restart-$current_time.log

cd deploy/local/live/
#cd deploy/tucson/

echo "Saving logs to" "$file_name"
docker-compose logs --no-color --tail 100 > $file_name
echo "Stopping LOVE"
docker-compose down
echo "Restarting LOVE"
docker-compose up -d

cd -
