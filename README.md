# Performance test of Hyperledger Fabric

## Dependencies

- Fabric `v2.4.6`
- Caliper `v0.5.0`

## How to use

See `fabric/scripts/fabric-samples/test-network/how-to-use.txt`.

I modified the scripts to support flexible orgs-adding feature, the entry is in `mynetwork.sh`, so remember to use `mynetwork.sh` instead of `network.sh`.

Also, I provide a bash script `auto-test.sh` to easily execute the whole test workflow.

## Results

See report files in `fabric/scripts/caliper-benchmarks`.

The name of report is formatted as `report-[m]p[n]o.html`, `m` is the number of peers, and `n` is the number of orderers. Currently, `n` is always 1.

## Speed up chaincode installation

You can change npm source for speeding up chaincode installation, and build `hyperledger/fabric-nodeenv` docker image manually.

See `fabric-chaincode-node-2.4.2/docker/fabric-nodeenv`, modify `build.sh` as follows:

```sh
if [ -f package-lock.json -o -f npm-shrinkwrap.json ]; then
    npm ci --only=production --registry=https://registry.npmmirror.com
else
    npm install --production --registry=https://registry.npmmirror.com
fi
```