kubectl apply -f .
sleep 10

# AUXTEL
kubectl apply -f simulators/simulator-atcs-deployment.yml
sleep 2
kubectl apply -f producers/producer-atdome-deployment.yml
kubectl apply -f producers/producer-atmcs-deployment.yml
sleep 2
kubectl apply -f producers/producer-ataos-deployment.yml
kubectl apply -f producers/producer-athexapod-deployment.yml
sleep 2
kubectl apply -f producers/producer-atpneumatics-deployment.yml
kubectl apply -f producers/producer-atcamera-deployment.yml
sleep 2
kubectl apply -f producers/producer-atdometrajectory-deployment.yml
kubectl apply -f producers/producer-atheaderservice-deployment.yml
sleep 2
kubectl apply -f producers/producer-atarchiver-deployment.yml
sleep 10

# MAINTEL
kubectl apply -f simulators/simulator-mtcs-deployment.yml
sleep 2
kubectl apply -f producers/producer-mtdome-deployment.yml
kubectl apply -f producers/producer-mtmount-deployment.yml
sleep 2
kubectl apply -f producers/producer-mtaos-deployment.yml
kubectl apply -f producers/producer-mthexapod-1-deployment.yml
kubectl apply -f producers/producer-mthexapod-2-deployment.yml
sleep 2
kubectl apply -f producers/producer-mtrotator-deployment.yml
kubectl apply -f producers/producer-mtcamera-deployment.yml
sleep 2
kubectl apply -f producers/producer-mtdometrajectory-deployment.yml
kubectl apply -f producers/producer-mtheaderservice-deployment.yml
sleep 2
kubectl apply -f producers/producer-mtm1m3-deployment.yml
sleep 2
kubectl apply -f producers/producer-mtm2-deployment.yml
sleep 10

#SCRIPTQUEUES
kubectl apply -f simulators/simulator-scriptqueue-deployment.yml
sleep 2
kubectl apply -f producers/producer-mtscriptqueue-deployment.yml
kubectl apply -f producers/producer-atscriptqueue-deployment.yml
sleep 10

#WATCHER
kubectl apply -f simulators/simulator-watcher-deployment.yml
sleep 2
kubectl apply -f producers/producer-watcher-deployment.yml

#WEATHER STATION
kubectl apply -f simulators/simulator-weatherstation-deployment.yml
sleep 2
kubectl apply -f producers/producer-weatherstation-1-deployment.yml
