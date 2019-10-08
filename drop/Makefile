all:
	python3 plot.py
test:
	 ${NPF_PATH}/npf-compare.py "rsspp+rss:RSS" rsspp+sprayer:Sprayer "rsspp+pipeline,queue:Software Shared Queue" "rsspp+pipeline,rr:Software RR Queue" "rsspp+pipeline,flowrr:Software Stateful RR" "rsspp+pipeline,flowrr,AWARE=1:Software Stateful Load" "rsspp+pipeline,queue:Software Shared Queue" "rsspp+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} --variables "QUEUE=[1-16]" --show-full --output --output-columns x raw --graph-filename drop-kthmorningquad/.pdf --tags kthmorningquad  --graph-size 6 3.5 --config n_runs=3 --variables TIMING=1 W=300 FREQ=1000 --tags fnt --result-path ".npf_results" ${NPF_FLAGS}
