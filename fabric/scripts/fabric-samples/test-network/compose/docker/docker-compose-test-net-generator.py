num_of_peer = 16

for i in range(num_of_peer):
    tmp_config = """
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

version: '3.7'
services:
"""
    for j in range(i+1):
        tmp_config += """
  peer0.org""" + str(j+1) + """.example.com:
    container_name: peer0.org""" + str(j+1) + """.example.com
    image: hyperledger/fabric-peer:latest
    labels:
      service: hyperledger-fabric
    environment:
      #Generic peer variables
      - CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock
      - CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=fabric_test
    volumes:
      - ./docker/peercfg:/etc/hyperledger/peercfg
      - ${DOCKER_SOCK}:/host/var/run/docker.sock
        
"""
    tmp_config += """
  cli:
    container_name: cli
    image: hyperledger/fabric-tools:latest
    volumes:
      - ./docker/peercfg:/etc/hyperledger/peercfg    
"""
    with open(str(j+1) + "-docker-compose-test-net.yaml", "w+") as f:
        f.write(tmp_config)