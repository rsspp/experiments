include ../includes/Makefile.include

.NOTPARALLEL:

all: test graph

graph:
	python3 plot.py

test:
	 ${NPF_PATH}npf-compare.py rsspp+rss:RSS rsspp+sprayer:Sprayer "rsspp+pipeline,queue:Software Shared Queue" "rsspp+pipeline,rr:Software RR Queue" "rsspp+pipeline,flowrr:Software Stateful RR" "rsspp+pipeline,flowrr,AWARE=1:Software Stateful Load" "rsspp+dynamicmetron:Metron Dynamic" "rsspp+pianorss,BALANCE_PERIOD=100:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --variables "QUEUE=8" --show-full --output --graph-filename latency-kthmorningquad.pdf --tags kthmorningquad ${NPF_FLAGS} --graph-size 7 4.5 --variables "GEN_RATE=[2000000000-34000000000#2000000000]" W=600 --tags quad rate --config n_runs=3 --output-columns x raw --build-folder ~/npf/build/ --result-path .npf_results_kthquad --max-results --no-graph-time
