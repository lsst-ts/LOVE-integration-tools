#!/bin/bash
echo  'Copying fixtures and thumbnails from dev.love into ./fixtures'
rm -rf fixtures
mkdir fixtures
cmd="source local_env.sh; docker-compose run --rm  manager python manage.py dumpdata ui_framework.view > test.json"
ssh love@dev.love.inria.cl $cmd
scp love@dev.love.inria.cl:~/test.json fixtures
scp -r love@dev.love.inria.cl:~/media fixtures/media

# copy everything into the live mode version

echo "Replacing local data"
sudo rm -rf db_data
sudo rm -f media/thumbnails/*
manager=../../../LOVE-manager
cp fixtures/test.json  $manager/manager/ui_framework/fixtures/initial_data.json
rm $manager/manager/media/thumbnails/*.png

echo
echo "Available thmbnails before copying: "
ls $manager/manager/media/thumbnails

cp fixtures/media/thumbnails/*.png  $manager/manager/media/thumbnails/.
rm -rf ../local/live/media
cp -r fixtures/media ../local/live/media
echo
echo "Available thmbnails after copying: "
ls $manager/manager/media/thumbnails
echo
