all: plot

graph: plot.py
	python3 plot.py

test:
	 ${NPF_PATH}/npf-compare.py "rsspp+rss:RSS" "rsspp+sprayer,shared:Sprayer" "rsspp+rsspp:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} dut=nslrack14-100G,nic=0 --show-full --graph-filename ./nat/nat-kthmorning-cx5.pdf --tags promisc --variables ITERATION_TIME=1 TIMING=1 --no-build --no-build-deps fastclick --graph-size 6 3 --max-results --output --output-columns x raw --variables W=0 --tags nat qtest kthmorningquad --config n_runs=1 --build-folder ~/npf/build/ --results-path .npf_results.qtest
