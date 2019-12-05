#Migration

This tests uses RSS with either the RSS++ per-group flow table, or a unique hash table, and study the latency and throughput over time. Because every 2 seconds, we add one more core, leading to flow migrations.

This test does not use the trace but 1024 concurrent UDP flows of 1500 bytes, with a duration of 1000 packets. This was done to precisely control the number of flows.

make test will run the test using NPF and ../dpdk.testie

make graph will do the plot using plot.py
