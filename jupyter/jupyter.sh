#!/usr/bin/env bash

# Source this file when starting the container to set it up

echo "#"
echo "# Loading LSST Stack"
. /opt/lsst/software/stack/loadLSST.bash
setup lsst_distrib
echo "#"
echo "# Loading sal environment"
. repos/ts_sal/setup.env
echo "#"
echo "# Setting up sal, salobj and scriptqueue"

setup ts_xml -t current
setup ts_sal -t current
setup ts_salobj -t current
setup ts_scriptqueue -t current
setup ts_ATDome -t current
setup ts_ATDomeTrajectory -t current
setup ts_standardscripts -t current
setup ts_externalscripts -t current

cd /home/saluser/repos
git clone https://github.com/lsst-ts/ts_watcher.git
cd ts_watcher
setup -r .
scons install declare

cd /home/saluser/
/bin/bash --rcfile /home/saluser/.bashrc
unset LSST_DDS_IP
make_idl_files.py GenericCamera
jupyter lab --no-browser --port=1234 --ip=0.0.0.0 --allow-root --NotebookApp.token='' 