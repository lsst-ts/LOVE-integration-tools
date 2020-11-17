# Deployment In La Serena

## 1. Prepare deployment
### 1.1. Copy required files
Copy the docker-compose and configuration files to the machine <USER>@<SERVER>:

```bash
scp deploy/laserena/docker-compose.yml <USER>@<SERVER>:.
scp deploy/laserena/.env <USER>@<SERVER>:.
scp deploy/laserena/nginx.conf <USER>@<SERVER>:.
scp deploy/laserena/ospl.xml <USER>@<SERVER>:.
scp deploy/laserena/config <USER>@<SERVER>:.
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
```bashM
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
