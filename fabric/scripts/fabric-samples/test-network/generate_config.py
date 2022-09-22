import sys

num_of_peer = int(sys.argv[1])

if num_of_peer is None or num_of_peer <= 0:
    print("error args ..")
    exit(-1)

tmp_config = """
# Definition of nodes
# addr address for node
# tls_ca_cert tls cert
"""

for i in range(num_of_peer):
    tmp_config += """
peer""" + str(i+1) + """: &peer""" + str(i+1) + """
  addr: localhost:""" + str(i+7) + """051
  tls_ca_cert: ./organizations/peerOrganizations/org""" + str(i+1) + """.example.com/peers/peer0.org""" + str(i+1) + """.example.com/msp/tlscacerts/tlsca.org""" + str(i+1) + """.example.com-cert.pem
"""

tmp_config += """
orderer1: &orderer1
  addr: localhost:7050
  tls_ca_cert: ./organizations/ordererOrganizations/example.com/msp/tlscacerts/tlsca.example.com-cert.pem

# Peer Nodes to interact with as endorsement Peers
endorsers:
"""

for i in range(num_of_peer):
    tmp_config += "  - *peer" + str(i+1) + "\n"

tmp_config += """

# Peer Nodes to interact with as Commit Peers as listening
committers: 
"""

for i in range(num_of_peer):
    tmp_config += "  - *peer" + str(i+1) + "\n"

tmp_config += """
# we might support multi-committer in the future for more complex test scenario.
# i.e. consider tx committed only if it's done on >50% of nodes. 
# Give your commit Threshold as numbers for peers here.
commitThreshold: """ + str(int(num_of_peer/2)+1) + """

# orderer Nodes to interact with
orderer: *orderer1

# Invocation configs
channel: mychannel
chaincode: basic
# chain code args below, in a list of str
# we provides 3 kinds of randmon
# uuid
# randomString$length
# randomNumber$min_$max
args:
  - CreateAsset
  - uuid
  - randomString8
  - randomNumber0_50
  - randomString8
  - randomNumber0_50
# Tx submiter information
mspid: Org1MSP
private_key: ./organizations/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/priv_sk
sign_cert: ./organizations/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/signcerts/User1@org1.example.com-cert.pem
# network traffic control
num_of_conn: 10
client_per_conn: 10

"""

with open("config.yaml", "w+") as f:
    f.write(tmp_config)