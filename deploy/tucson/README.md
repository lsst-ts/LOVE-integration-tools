# Deployment In Tucson

## 1. Prepare deployment
### 1.1. Copy required files
Copy the docker-compose and configuration files to the machine <USER>@<SERVER>:

```bash
scp deploy/tucson/docker-compose.yml <USER>@<SERVER>:.
scp deploy/tucson/.env <USER>@<SERVER>:.
scp deploy/tucson/nginx.conf <USER>@<SERVER>:.
scp deploy/tucson/ospl.xml <USER>@<SERVER>:.
scp deploy/tucson/config <USER>@<SERVER>:.
```

### 1.2. (Optional) Change services versions
In order to modify the version of a service edit the version of the desired service on the corresponding docker-compose file, on the `image` section.

For example, to run the `frontend` service's version `x.y.z`, change the image tag from `master` to `x.y.z`, as following:
```yaml
frontend:
  ...
  image: inriachile/love-frontend:master
  ...
```

into

```yaml
frontend:
  ...
  image: inriachile/love-frontend:x.y.z
  ...
```


## 2. Launch services
### 2.1 Launch LOVE services
```bash
ssh <USER>@<SERVER>:.
source local_env.sh
docker-compose pull
docker-compose down -v
docker-compose up -d
```

### 2.2. (Optional) Launch Simulators
```bash
ssh <USER>@<SERVER>:.
docker-compose -f docker-compose-simulator.yml pull
docker-compose -f docker-compose-simulator.yml down -v
docker-compose -f docker-compose-simulator.yml up -d
```





---

## (Old) Running the ATDome simulator


1. Clone the docker-compose-ops repo: https://github.com/LSST-IT/docker-compose-ops
2. Copy the `opsl.xml` in the repository root folder. The `<NetworkInterfaceAddress>auto</NetworkInterfaceAddress>` should work most of the time.
3. `cd AT_Simulators`
4. In the `docker-compose.yml` comment the all of the code of the `atptg-sim` and `simulation-tests` services. The `atptg-sim` at this day is a private image and the `simulation-test` will run in the next step.
5. Open the  `simulation-test` container in an interactive session:
```bash
 docker run -it --network host -e LSST_DDS_DOMAIN=$LSST_DDS_DOMAIN -e OSPL_URI=$OSPL_URI -v $OSPL_CONFIG_PATH:$OSPL_MOUNT_POINT --name simulation-tests lsstts/simulation_tests:latest
```
6. Open `ipython`
7. Check the heartbeat works first:
```python
import asyncio
from lsst.ts import salobj

import SALPY_ATDome

r = salobj.Remote(SALPY_ATDome, index=1)

await r.evt_heartbeat.next(flush=True, timeout=5)

```

8. Set the CSC in enabled state:
```python
await r.cmd_start.start(timeout=30)
await salobj.set_summary_state(r, salobj.State.ENABLED)
```
Alternatively, this is supposed to work also with:
```python
await r.cmd_start.start(timeout=30)
await r.cmd_enable.start(timeout=30)
```
9. Now you can send commands, for instance:
```python
   r.cmd_moveAzimuth.set(azimuth=180.)
   await r.cmd_moveAzimuth.start()
```
