# Dynamic scaling

The purpose of this experiment is to compare RSS++'s scaling with Metron. Metron is not load-aware, and its classes may not be a good split of traffic at all, as it depends on the configuration of the operator. Also, RSS++ is made for a better information delay.

As all DPDK tests, this experiment use NPF's testie ../dpdk.testie.

The Makefile will launch the right command line:
Systems : "rsspp+rss:RSS" "rsspp+dynamicmetron:Metron" "rsspp+pianorss,BALANCE_PERIODE=100:RSSPP"
Trace: kthmorningquad 
Variables : QUEUE=15 W=300 TIMING=100 AUTOSCALE=1 (of course autoscaling is enabled)
Tags : nolatlog (no latency tracking) iterative (study of metrics over time) promisc largemem (see below) sfnt (enable the slow function curve to modulate the TX)
Variables : "DPDKMEM=127000,2000" "LIMIT=15000000" PKTGEN_REPLAY_TIME=70 PKTGEN_REPLAY_COUNT=3 to load the most packets from memory as possible. In this test the fact that we replay the test would impact the peformance of the techniques, so do it as less as possible. The spike you see is an artifact of the experiment, it is when a second replay starts.

make graph will then plot the graph.  The CSVs for this tests are provided.
