# Integration Tools

This repository contains scripts and tools to integrate applications from the different development repositories, in order to be used for deployment purposes.

## Expected folder structure
The LOVE repositories are expected to be at the same level under the same parent folder. Additionally the root folder should contain a folder named `tsrepos`, containing the LSST repositories `salobj`, `ts_sal` and `ts_xml`.  For example:

* LOVE
  - LOVE-frontent
  - LOVE-backend
  - integration-tools
  - tsrepos
    - salobj
    - ts_sal
    - ts_xml

## Files:
This repository contains the following:
* ***deploy:*** contains the `docker-compose.yml` and `.env` files needed for deploying
  * ***docker-compose.yml:*** these files define the services that will be ran with docker
  * ***.env:*** these files contains the environment variables pointing to the different project paths
  * ***prod:*** contains the `docker-compose.yml` and `.env` files for deploying in the production environment
  * ***dev:*** contains the `docker-compose.yml` and `.env` files for development purposes
* ***nginx:*** contains NGINX configuration files in order to coordinate HTTP requests between the django server and the frontend.
