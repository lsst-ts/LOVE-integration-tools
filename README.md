# LOVE-integration-tools instructions

The LOVE-integration-tools repository provides scripts and tools to integrate the applications from the different development repositories, in order to be used for development and deployment purposes.
See the full documentation here: https://lsst-ts.github.io/LOVE-integration-tools/html/index.html

## Directory tree

```
.
├── deploy              # Config scripts for all of the deployment environments
│   ├── linode            # Monolith configuration with simulators and LOVE stack
│   ├── local             # Monolith config for local configurations
│   │   ├── build           # Uses locally built docker images
│   │   ├── lite            # Uses local frontend and a remote backend
│   │   ├── live            # Local frontend, backend and simulators
│   │   ├── live-csc        # As live, but backend is split by CSC instead of message type
│   ├── summit           # Monolith config for the deployment at the Summit lba
│   └── tucson           # Monolith config for the deployment at the Tucson lab
├── docs               # Built docs files to be served as a static page
├── docsrc             # Source files of the docs
├── jupyter            # Jupyter notebooks to send SAL commands for manual tests
└── tests              # Integration and load tests and similar
```

## The `deploy` folder

This directory contains different the files needed for deployment environments. Each environment is enclosed in a directory, with the possibility of having sub-environments in nested sub-directories, following a tree structure.

### Environment content

Each environment contains the following types of files:

- `docker-compose.yml:` these files define the services that will be run with docker
- `.env:` these files contains the environment variables with different configuration parameters, such as the different project paths, network configuration, among others.
- `nginx` directory: contains NGINX configuration files (`default.conf` and `Dockerfile`) in order to coordinate HTTP requests between the django server and the frontend.
  - `default.conf`: Nginx configuraiton file that defines the routing and other network configuraitons
  - `Dockerfile`: to build the docker image needed to run the Nginx service

**IMPORTANT:** make sure to redefine the secrets defined by the `.env` files for real production environments. You can do that by defining them in your environment directly, if the variables are defined in your environment they will have priority over the values defines in the `.env` files. See the `.env` files to see which variables should be overriden, search for the following comment line:

`## (Dummy) secrets, make sure to replace them in real production environments!`

### Environments

The `deploy` directory is structured as follows:

- **linode**: corresponds to the deployment in Inria linode machines, for demonstration purposes
  - `docker-compose-dev.yml`: deploys the development version, using docker images pulled from dockerhub tagged as `dev`
  - `docker-compose.yml`: deploys the development version, using docker images pulled from dockerhub tagged as
- **local**: contains environments for local development. Building images from local repositories, located as described in "Expected folder structure"
  - **build**: contains the files for deploying the system by building production docker images from local repositories.
  - **live**: contains the files for deploying the system by building development docker images from local repositories. These images work by mounting the source code of their corresponding repositories as a volume, rather than copying it. They also use development or "live" modes for running some of the applications, Manager and Frontend.
- **tucson**: corresponds to the deployment in the machines in Tucson. The configuration is different in the network configuration, in order to connect to the SAL components.

## Jenkinsfile

Defines the jobs to be executed by a Jenkins machine when changes are committed in this repository. These jobs include:

- Building and pushing Nginx docker images to Dockerhub, when there are changes in the corresponding `nginx` directories
- Pulling images, and redeploying the LOVE services in the production environments, when there are changes in the definition of the environments (or if triggered by the jobs that update the docker image in each related repo). Currently, this is only done for the Linode environments (master and develop)

---

## Running the project

### Building from local repositories


For this you need to have the following tree structure:
```
.
├── LOVE-commander
├── LOVE-frontend
├── LOVE-integration-tools
├── LOVE-manager
├── LOVE-producer
├── LOVE-simulator
├── ts_externalscripts      # for `linode` and `local/live` environments only
└── ts_standardscripts      # for `linode` and `local/live` environments only
---

You can run a locally-built version of the application as

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
docker-compose -f docker-compose-master.yml down -v
docker-compose -f docker-compose-master.yml build
docker-compose -f docker-compose-master.yml up -d
```

If there is a problem loading the static files from the browser, try deleting the docker volumes:

```
docker-system prune --volumes
```

#### Develop branch version

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

---

## Update documentation

We provide a docker image and a docker-compose file in order to load the LOVE-integration-tools locally to build the documentation.

This docker-compose does not copy the code into the image, but instead it mounts the repository inside the image, this way you can edit the code from outside the docker container with no need to rebuild or restart.

### Load and get into the docker image

Follow these instructions to run the application in a docker container and get into it:

```
docker-compose up -d
docker-exec tools bash
```

### Build documentation

Once inside the container you will be in the `/usr/src/love/` folder, where you can move into the `docsrc` folder and build the documentation as follows:

```
cd docsrc
./create_docs.sh
```

--

## Testing

Tests are available in the `tests` folder

### Integration testing

To run the integration tests against the dev environment, run the following commands from the `tests/e2e` directory:

#### Headless:

`docker-compose up --exit-code-from cypress`

#### Interactive:

`docker-compose -f docker-compose.yml -f cy-open.yml up --exit-code-from cypress`

### Load testing

To run the loads tests run the following commands from the `tests/load` directory:

`docker-compose up -d`

Then open `localhost:1234` on your web browser and enter into jupyter using the password `jupyter`.
In jupyter open the file `notebooks/stress_test.ipynb` and run all the cells

The tests are also available from any jupyter installation along side a love deployment. For example `deploy/local/live`, depending on the case you may need to change the `manager_location` variable on the first cell accordingly (see comments in cell).
