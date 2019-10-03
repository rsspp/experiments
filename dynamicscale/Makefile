include ../includes/Makefile.include

.NOTPARALLEL:

all: test graph


graph:
	python3 plot.py

test:
	 ${NPF_PATH}/npf-compare.py "rsspp+rss:RSS" "rsspp+dynamicmetron:Metron" "rsspp+pianorss,BALANCE_PERIODE=100:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} --graph-filename ./kthmorning-cx5.pdf --tags kthmorningquad --use-last --graph-size 7 4.5 --config n_runs=1 --variables BVERBOSE=0 --no-build-deps fastclick --max-results --variables BVERBOSE=0 QUEUE=15 W=300 TIMING=100 --tags nolatlog iterative promisc largemem sfnt --variables AUTOSCALE=1 --config "var_lim={}" --output --variables "DPDKMEM=127000,2000" "LIMIT=15000000" PKTGEN_REPLAY_TIME=70 PKTGEN_REPLAY_COUNT=3 ${NPF_FLAGS}
