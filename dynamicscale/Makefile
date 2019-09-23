all:
	python3 plot.py

test:
	~/npf/npf-compare.py "metron+rss:RSS" "metron+dynamicmetron:Metron" "rsspp+pianorss,BALANCE_PERIODE=100:RSSPP" --testie ../dpdk.testie --cluster client=nslrack12-100G,nic=1 p=nslrack14-100G,nic=0 server=nslrack14-100G,nic=0 --show-full --graph-filename ~/workspace/rss-experiments/dynamicscale/kthmorning-cx5.pdf --tags kthmorningquad --no-build --use-last --graph-size 7 4.5 --config n_runs=1 --variables BVERBOSE=0 --no-build-deps fastclick --max-results --variables BVERBOSE=0 QUEUE=15 W=300 TIMING=100 --tags nolatlog iterative promisc largemem sfnt --show-cmd --variables AUTOSCALE=1 --config "var_lim={}" --output --force-retest --variables "DPDKMEM=127000,2000" "LIMIT=15000000" PKTGEN_REPLAY_TIME=70 PKTGEN_REPLAY_COUNT=3 --build-folder ~/npf/build/
