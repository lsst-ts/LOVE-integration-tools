# LOVE-integration-tools instructions

The LOVE-integration-tools repository provides scripts and tools to integrate the applications from the different development repositories, in order to be used for development and deployment purposes.
See the full documentation here: https://love-integration-tools.lsst.io/.

## Directory tree

```
.
├── deploy              # Config scripts for all of the deployment environments
│   ├── base              # Monolith config for the deployment at the Base Test Stand
│   ├── k8s               # Configurations for deploying the system in a Kubernetes cluster
│   ├── local             # Monolith config for local configurations
│   │   ├── build           # Uses locally built docker images
│   │   ├── lite            # Uses local frontend and a remote backend
│   │   ├── live            # Local frontend, backend and simulators
│   │   ├── live-csc        # As live, but backend is split by CSC instead of message type
│   ├── summit            # Monolith config for the deployment at the Summit Bare Metal Machine #1
│   ├── summit2           # Monolith config for the deployment at the Summit Bare Metal Machine #2
│   └── tucson            # Monolith config for the deployment at the Tucson Test Stand
├── docsrc              # Source files of the docs
├── jupyter             # Jupyter notebooks to send SAL commands for manual tests
└── tests               # Integration and load tests and similar
```

## The `deploy` folder

This directory contains the different files needed for deployment environments. Each environment is enclosed in a directory, with the possibility of having sub-environments in nested sub-directories, following a tree structure.

### Environment content

Each environment contains the following types of files:

- `docker-compose.yml:` these files define the services that will be run with docker.
- `.env:` these files contains the environment variables with different configuration parameters, such as the different project paths, network configuration, among others.
- `nginx.conf`: nginx configuration file that defines the routing and other network configurations.

**IMPORTANT:** make sure to redefine the secrets defined by the `.env` files for real production environments. You can do that by defining them in your environment directly, if the variables are defined in your environment they will have priority over the values defines in the `.env` files. See the `.env` files to see which variables should be overriden, search for the following comment line:

`## (Dummy) secrets, make sure to replace them in real production environments!`

### Environments

The `deploy` directory is structured as follows:

- **local**: contains environments for local development. Building images from local repositories, located as described in "Directory tree".
  - **build**: contains the files for deploying the system by building production docker images from local repositories.
  - **live**: contains the files for deploying the system by building development docker images from local repositories. These images work by mounting the source code of their corresponding repositories as a volume, rather than copying it. They also use development or "live" modes for running some of the applications, Manager and Frontend.
  - **live-csc (recommended)**: same as live, but using backend is split by CSC.
  - **lite**: similar to live ones, but contains the files for just deploying a locally built Frontend application, which can connect to a remote backend. Not recommended, to be used mainly by advanced users.
- **summit**: corresponds to the deployment in the machines in the Summit Bare Metal Machine #1. The configuration is different in the network configuration, in order to connect to the SAL components.
- **summit2**: same as summit, but for Bare Metal Machine #2.
- **base**: corresponds to the deployment in the machines in the Base Test Stand. The configuration is different in the network configuration, in order to connect to the SAL components.
- **tucson**: corresponds to the deployment in the machines in the Tucson Test Stand. The configuration is different in the network configuration, in order to connect to the SAL components.
- **k8s**: contains the files for deploying the system in a Kubernetes cluster. The configuration is different in the network configuration, in order to connect to the SAL components.

## Jenkinsfile

Defines the jobs to be executed by a Jenkins machine when changes are committed in this repository. There is currently only one job:

- Building and pushing the documentation to [love-integration-tools.lsst.io](https://love-integration-tools.lsst.io).

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
```

You can run a locally-built version of the application as

```
cd LOVE-integration-tools/deploy/local/live-csc
docker-compose down -v
docker-compose build
docker-compose up -d
```

If there is a problem loading the static files from the browser, try deleting the docker volumes:

```
docker system prune --volumes
```

---

## Update documentation

We provide a docker image and a docker-compose file in order to load the LOVE-integration-tools locally to build the documentation.

This docker-compose does not copy the code into the image, but instead it mounts the repository inside the image, this way you can edit the code from outside the docker container with no need to rebuild or restart.

### Load and get into the docker image

Follow these instructions to run the application in a docker container and get into it:

```
cd docsrc
docker-compose up -d
docker-compose exec tools bash
```

### Build documentation

Once inside the container you will be in the `/usr/src/love/` folder, where you can move into the `docsrc` folder and build the documentation as follows:

```
cd docsrc
./create_docs.sh
```

---

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

---

## Linting & Formatting

This code uses pre-commit to maintain `black` formatting, `isort` and `flake8` compliance. To enable this, run the following commands once (the first removes the previous pre-commit hook):

```
git config --unset-all core.hooksPath
generate_pre_commit_conf
```

For more details on how to use `generate_pre_commit_conf` please follow: https://tssw-developer.lsst.io/procedures/pre_commit.html#ts-pre-commit-conf.
