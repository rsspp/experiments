all: plot

plot: plot.py
	python3 plot.py

test:
	~/npf/npf-compare.py "metron+rss:RSS" "metron+sprayer,shared:Sprayer" "metron+rsspp:RSSPP" --testie ../dpdk.testie --cluster client=nslrack12-100G,nic=1 p=nslrack14-100G,nic=0 server=nslrack14-100G,nic=0 dut=nslrack14-100G,nic=0 --show-full --graph-filename ~/workspace/rss-experiments/nat/nat-kthmorning-cx5.pdf --tags promisc --variables ITERATION_TIME=1 TIMING=1 --no-build --no-build-deps fastclick --graph-size 6 3 --max-results --output --output-columns x raw --variables W=0 --tags nat qtest kthmorningquad --config n_runs=1 --build-folder ~/npf/build/ --results-path .npf_results.qtest
