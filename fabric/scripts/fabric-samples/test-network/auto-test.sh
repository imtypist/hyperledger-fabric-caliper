#!/bin/bash

START_PEER=$1
END_PEER=$2

for((i=$START_PEER; i<=$END_PEER; i+=2))
do
NUM_OF_PEER=$i
# update config
python3 generate_config.py $NUM_OF_PEER
cd configtx && python3 generate_configtx.py $NUM_OF_PEER && cd ..

# setup network and channel
./mynetwork.sh up createChannel -numofpeer $NUM_OF_PEER

# deploy chaincode
./mynetwork.sh deployCC -ccn fabcar -ccp ../../caliper-benchmarks/src/fabric/samples/fabcar/node/ -ccl javascript -numofpeer $NUM_OF_PEER

# update benchconfig
cd ../../caliper-benchmarks/benchmarks/samples/fabric/fabcar/ && python3 generate_config.py $NUM_OF_PEER

# run caliper test
cd ../../../../../../../caliper-0.5.0/ && node ./packages/caliper-cli/caliper.js launch manager --caliper-workspace ../fabric/scripts/caliper-benchmarks/ --caliper-benchconfig benchmarks/samples/fabric/fabcar/config.yaml --caliper-networkconfig networks/fabric/test-network.yaml

# close network and remove containers
cd ../fabric/scripts/fabric-samples/test-network/ && ./mynetwork.sh down -numofpeer $NUM_OF_PEER

# save result
cd ../../caliper-benchmarks/ && mv report.html report-${NUM_OF_PEER}p1o.html || exit

# back to test-network dir
cd ../fabric-samples/test-network/
done