include ../includes/Makefile.include

.NOTPARALLEL:

all: test graph

graph: plot.py
	python3 plot.py

test:
	${NPF_PATH}/npf-compare.py  "rsspp+rss,rl:RSS FW" "rsspp+sprayer,rl:Sprayer FW" "rsspp+pianorss,rl:RSSPP FW" "rsspp+rss,rl,nat:RSS FW+NAT" "rsspp+sprayer,rl,nat,shared:Sprayer FW+NAT" "rsspp+pianorss,rl,nat:RSSPP FW+NAT" "rsspp+rss,rl,nat,frl:RSS FW+NAT+DPI" "rsspp+sprayer,rl,nat,shared,frl:Sprayer FW+NAT+DPI" "rsspp+pianorss,rl,nat,frl:RSSPP FW+NAT+DPI" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --show-full --graph-filename nat-kthmorning-cx5/.pdf --tags promisc --variables ITERATION_TIME=1 TIMING=1 QUEUE=16 PKTGEN_REPLAY_TIME=90 PKTGEN_REPLAY_COUNT=20 GEN_BLOCKING=1 SAMPLE=100 --graph-size 6 3 --output --output-columns x raw --variables W=0 --tags kthmorningquad replay iterative fntgrow --config n_runs=1 var_sync="{}" ${NPF_FLAGS}
