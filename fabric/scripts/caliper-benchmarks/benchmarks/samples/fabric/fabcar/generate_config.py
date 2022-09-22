import sys

num_of_peer = int(sys.argv[1])

tmp_config = """
test:
  name: Fabcar benchmark
  description: """+ str(num_of_peer) +""" peer, 1 orderer
  workers:
    number: 5
  rounds:
"""

initTps = [i for i in range(100, 1001, 100)]

queryTps = [i for i in range(200, 2001, 200)]

# initPKG
for i in initTps:
    tmp_config += """
    - label: initPKG (tps="""+ str(i) +""")
      txDuration: 10
      rateControl:
          type: fixed-rate
          opts:
            tps: """+ str(i) +"""
      workload:
        module: benchmarks/samples/fabric/fabcar/initPKG.js    
"""

# initVID
for i in initTps:
    tmp_config += """
    - label: initVID (tps="""+ str(i) +""")
      txDuration: 10
      rateControl:
          type: fixed-rate
          opts:
            tps: """+ str(i) +"""
      workload:
        module: benchmarks/samples/fabric/fabcar/initVID.js
"""

# queryPKG
for i in queryTps:
    tmp_config += """
    - label: Query PKG (tps="""+ str(i) +""")
      txDuration: 10
      rateControl:
          type: fixed-rate
          opts:
            tps: """+ str(i) +"""
      workload:
        module: benchmarks/samples/fabric/fabcar/queryPKG.js
        arguments:
          assets: 500
"""

# queryVID
for i in queryTps:
    tmp_config += """
    - label: Query VID (tps="""+ str(i) +""")
      txDuration: 10
      rateControl:
          type: fixed-rate
          opts:
            tps: """+ str(i) +"""
      workload:
        module: benchmarks/samples/fabric/fabcar/queryVID.js
        arguments:
          assets: 500
"""

with open("config.yaml", "w+") as f:
    f.write(tmp_config)