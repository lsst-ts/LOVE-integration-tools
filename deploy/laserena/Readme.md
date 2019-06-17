# Running the ATDome simulator


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
