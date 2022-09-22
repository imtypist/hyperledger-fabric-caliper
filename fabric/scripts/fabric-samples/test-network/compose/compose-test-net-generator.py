num_of_peer = 16

header_block="""
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

version: '3.7'

volumes:
  orderer.example.com:

"""

order_block="""

networks:
  test:
    name: fabric_test

services:

  orderer.example.com:
    container_name: orderer.example.com
    image: hyperledger/fabric-orderer:latest
    labels:
      service: hyperledger-fabric
    environment:
      - FABRIC_LOGGING_SPEC=INFO
      - ORDERER_GENERAL_LISTENADDRESS=0.0.0.0
      - ORDERER_GENERAL_LISTENPORT=7050
      - ORDERER_GENERAL_LOCALMSPID=OrdererMSP
      - ORDERER_GENERAL_LOCALMSPDIR=/var/hyperledger/orderer/msp
      # enabled TLS
      - ORDERER_GENERAL_TLS_ENABLED=true
      - ORDERER_GENERAL_TLS_PRIVATEKEY=/var/hyperledger/orderer/tls/server.key
      - ORDERER_GENERAL_TLS_CERTIFICATE=/var/hyperledger/orderer/tls/server.crt
      - ORDERER_GENERAL_TLS_ROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]
      - ORDERER_GENERAL_CLUSTER_CLIENTCERTIFICATE=/var/hyperledger/orderer/tls/server.crt
      - ORDERER_GENERAL_CLUSTER_CLIENTPRIVATEKEY=/var/hyperledger/orderer/tls/server.key
      - ORDERER_GENERAL_CLUSTER_ROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]
      - ORDERER_GENERAL_BOOTSTRAPMETHOD=none
      - ORDERER_CHANNELPARTICIPATION_ENABLED=true
      - ORDERER_ADMIN_TLS_ENABLED=true
      - ORDERER_ADMIN_TLS_CERTIFICATE=/var/hyperledger/orderer/tls/server.crt
      - ORDERER_ADMIN_TLS_PRIVATEKEY=/var/hyperledger/orderer/tls/server.key
      - ORDERER_ADMIN_TLS_ROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]
      - ORDERER_ADMIN_TLS_CLIENTROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]
      - ORDERER_ADMIN_LISTENADDRESS=0.0.0.0:7053
      - ORDERER_OPERATIONS_LISTENADDRESS=orderer.example.com:9443
      - ORDERER_METRICS_PROVIDER=prometheus
    working_dir: /root
    command: orderer
    volumes:
        - ../organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp:/var/hyperledger/orderer/msp
        - ../organizations/ordererOrganizations/example.com/orderers/orderer.example.com/tls/:/var/hyperledger/orderer/tls
        - orderer.example.com:/var/hyperledger/production/orderer
    ports:
      - 7050:7050
      - 7053:7053
      - 9443:9443
    networks:
      - test


"""

for i in range(num_of_peer):
    tmp_config = header_block
    for j in range(i+1):
        tmp_config += "  peer0.org" + str(j+1) + ".example.com:\n"
    tmp_config += order_block
    for j in range(i+1):
        tmp_config +="""
  peer0.org""" + str(j+1) + """.example.com:
    container_name: peer0.org""" + str(j+1) + """.example.com
    image: hyperledger/fabric-peer:latest
    labels:
      service: hyperledger-fabric
    environment:
      - FABRIC_CFG_PATH=/etc/hyperledger/peercfg
      - FABRIC_LOGGING_SPEC=INFO
      #- FABRIC_LOGGING_SPEC=DEBUG
      - CORE_PEER_TLS_ENABLED=true
      - CORE_PEER_PROFILE_ENABLED=false
      - CORE_PEER_TLS_CERT_FILE=/etc/hyperledger/fabric/tls/server.crt
      - CORE_PEER_TLS_KEY_FILE=/etc/hyperledger/fabric/tls/server.key
      - CORE_PEER_TLS_ROOTCERT_FILE=/etc/hyperledger/fabric/tls/ca.crt
      # Peer specific variables
      - CORE_PEER_ID=peer0.org""" + str(j+1) + """.example.com
      - CORE_PEER_ADDRESS=peer0.org""" + str(j+1) + """.example.com:""" + str(j+7) + """051
      - CORE_PEER_LISTENADDRESS=0.0.0.0:""" + str(j+7) + """051
      - CORE_PEER_CHAINCODEADDRESS=peer0.org""" + str(j+1) + """.example.com:""" + str(j+7) + """052
      - CORE_PEER_CHAINCODELISTENADDRESS=0.0.0.0:""" + str(j+7) + """052
      - CORE_PEER_GOSSIP_BOOTSTRAP=peer0.org""" + str(j+1) + """.example.com:""" + str(j+7) + """051
      - CORE_PEER_GOSSIP_EXTERNALENDPOINT=peer0.org""" + str(j+1) + """.example.com:""" + str(j+7) + """051
      - CORE_PEER_LOCALMSPID=Org""" + str(j+1) + """MSP
      - CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/msp
      - CORE_OPERATIONS_LISTENADDRESS=peer0.org""" + str(j+1) + """.example.com:""" + str(j+9444) + """
      - CORE_METRICS_PROVIDER=prometheus
      - CHAINCODE_AS_A_SERVICE_BUILDER_CONFIG={"peername":"peer0org""" + str(j+1) + """"}
      - CORE_CHAINCODE_EXECUTETIMEOUT=300s
    volumes:
        - ../organizations/peerOrganizations/org""" + str(j+1) + """.example.com/peers/peer0.org""" + str(j+1) + """.example.com:/etc/hyperledger/fabric
        - peer0.org""" + str(j+1) + """.example.com:/var/hyperledger/production
    working_dir: /root
    command: peer node start
    ports:
      - """ + str(j+7) + """051:""" + str(j+7) + """051
      - """ + str(j+9444) + """:""" + str(j+9444) + """
    networks:
      - test


"""
    # client_block
    tmp_config +="""
  cli:
    container_name: cli
    image: hyperledger/fabric-tools:latest
    labels:
      service: hyperledger-fabric
    tty: true
    stdin_open: true
    environment:
      - GOPATH=/opt/gopath
      - FABRIC_LOGGING_SPEC=INFO
      - FABRIC_CFG_PATH=/etc/hyperledger/peercfg
      #- FABRIC_LOGGING_SPEC=DEBUG
    working_dir: /opt/gopath/src/github.com/hyperledger/fabric/peer
    command: /bin/bash
    volumes:
        - ../organizations:/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations
        - ../scripts:/opt/gopath/src/github.com/hyperledger/fabric/peer/scripts/
    depends_on:

"""
    for j in range(i+1):
        tmp_config += "      - peer0.org" + str(j+1) + ".example.com\n"
    
    tmp_config +="""
    networks:
      - test

"""
    with open(str(i+1)+"-compose-test-net.yaml","w+") as f:
        f.write(tmp_config)