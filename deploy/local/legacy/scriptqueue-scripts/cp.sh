#!/bin/bash
function copy {
    cmd="docker-compose ps -q $1"
    echo $cmd
    docker cp $2 "$($cmd)":$3
}

copy scriptqueue-sim rotate_atdome.py /home/saluser/repos/ts_scriptqueue/tests/data/standard/