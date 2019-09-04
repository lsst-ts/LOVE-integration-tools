# LOVE-integration-tools instructions

This repository contains scripts and tools to integrate applications from the different development repositories, in order to be used for development and deployment purposes.

## Expected folder structure
The LOVE repositories are expected to be at the same level under the same parent folder, for example:

* LOVE
  - LOVE-frontent
  - LOVE-manager
  - LOVE-producer
  - LOVE-integration-tools
  - LOVE-simulator
---

## Content

### Deploy directory
This directory contains different the files needed for deployment environments. Each environment is enclosed in a directory, with the possibility of having sub-environments in nested sub-directories, following a tree structure.

#### Environment content
Each environment contains the following types of files:

  * `docker-compose.yml:` these files define the services that will be run with docker
  * `.env:` these files contains the environment variables with different configuration parameters, such as the different project paths, network configuration, among others.
  * `nginx` directory: contains NGINX configuration files (`default.conf` and `Dockerfile`) in order to coordinate HTTP requests between the django server and the frontend.
    * `default.conf`: Nginx configuraiton file that defines the routing and other network configuraitons
    * `Dockerfile`: to build the docker image needed to run the Nginx service

#### Environments
The `deploy` directory is structured as follows:
  * **linode**: corresponds to the deployment in Inria linode machines, for demonstration purposes
    * `docker-compose-dev.yml`: deploys the development version, using docker images pulled from dockerhub tagged as `dev`
    * `docker-compose.yml`: deploys the development version, using docker images pulled from dockerhub tagged as
  * **local**: contains environments for local development. Building images from local repositories, located as described in "Expected folder structure"
    * **build**: contains the files for deploying the system by building production docker images from local repositories.
    * **live**: contains the files for deploying the system by building development docker images from local repositories. These images work by mounting the source code of their corresponding repositories as a volume, rather than copying it. They also use development or "live" modes for running some of the applications, Manager and Frontend.
  * **tucson**: corresponds to the deployment in the machines in Tucson. The configuration is different in the network configuration, in order to connect to the SAL components.

### Jenkinsfile
Defines the jobs to be executed by a Jenkins machine when changes are committed in this repository. These jobs include:
* Building and pushing Nginx docker images to Dockerhub, when there are changes in the corresponding `nginx` directories
* Pulling images, and redeploying the LOVE services in the production environments, when there are changes in the definition of the environments (or if triggered by the jobs that update the docker image in each related repo). Currently, this is only done for the Linode environments (master and develop)

---

## Run the project
### Building from local repositories
For this you will need local clones of all the repositories in the same parent level as this repository (as explained in the "Expected folder structure" section above). In order to run the application follow these instructions:

```
cd LOVE-integration-tools/deploy/local/build
docker-compose down -v
docker-compose build
docker-compose up -d
```

If there is a problem loading the static files from the browser, try deleting the docker volumes:
```
docker-system prune --volumes
```

### Pulling images form Dockerhub
#### Master branch version
```
cd LOVE-integration-tools/linode
docker-compose down -v
docker-compose build
docker-compose up -d
```

If there is a problem loading the static files from the browser, try deleting the docker volumes:
```
docker-system prune --volumes
```

#### Develop branch version
```
cd LOVE-integration-tools/linode
docker-compose -f docker-compose-dev.yml down -v
docker-compose -f docker-compose-dev.yml build
docker-compose -f docker-compose-dev.yml up -d
```

If there is a problem loading the static files from the browser, try deleting the docker volumes:
```
docker-system prune --volumes
```
