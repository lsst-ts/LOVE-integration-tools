# Integration Tools

This repository contains scripts and tools to integrate applications from the different development repositories, in order to be used for development and deployment purposes.

## Expected folder structure
The LOVE repositories are expected to be at the same level under the same parent folder. Additionally the root folder should contain a folder named `tsrepos`, containing the LSST repositories `ts_salobj`, `ts_sal` and `ts_xml`.  For example:

* LOVE
  - LOVE-frontent
  - LOVE-manager
  - LOVE-producer
  - LOVE-integration-tools
  - tsrepos
    - salobj
    - ts_sal
    - ts_xml

## Files
This repository contains the following:
* ***deploy:*** contains the `docker-compose.yml` and `.env` files needed for deploying
  * ***docker-compose.yml:*** these files define the services that will be ran with docker
  * ***.env:*** these files contains the environment variables pointing to the different project paths
  * ***prod:*** contains the `docker-compose.yml` and `.env` files for deploying in the production environment
  * ***dev:*** contains the `docker-compose.yml` and `.env` files for development purposes
* ***nginx:*** contains NGINX configuration files in order to coordinate HTTP requests between the django server and the frontend.

---

## Run the project
### Build and run from local repositories
For this you will need local clones of all the repositories in the same parent level as this repository (as explained in the "Expected folder structure" section above). In order to run the application follow these instructions:

```
cd LOVE-integration-tools/deploy/prod
docker-compose build
docker-compose up -d
```

If there is a problem loading the static files from the browser, try deleting the docker volumes:
```
docker-system prune --volumes
```
