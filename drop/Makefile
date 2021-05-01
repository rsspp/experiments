include ../includes/Makefile.include

.NOTPARALLEL:

all: test graph

graph:
	python3 plot.py

test:
	 ${NPF_PATH}npf-compare.py "rsspp+rss:RSS" rsspp+sprayer:Sprayer "rsspp+pipeline,queue:Software Shared Queue" "rsspp+pipeline,rr:Software RR Queue" "rsspp+pipeline,flowrr:Software Stateful RR" "rsspp+pipeline,flowrr,AWARE=1:Software Stateful Load" "rsspp+pipeline,queue:Software Shared Queue" "rsspp+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --variables "QUEUE=[1-16]" --show-full --output --output-columns x raw --graph-filename drop-kthmorningquad/.pdf --tags kthmorningquad  --graph-size 6 3.5 --config n_runs=3 --variables TIMING=0 W=300 FREQ=1000 --result-path ".npf_results" ${NPF_FLAGS}

test_fw:
	 ${NPF_PATH}npf-compare.py "rsspp+rss:RSS" rsspp+sprayer:Sprayer "rsspp+pipeline,queue:Software Shared Queue" "rsspp+pipeline,rr:Software RR Queue" "rsspp+pipeline,flowrr:Software Stateful RR" "rsspp+pipeline,flowrr,AWARE=1:Software Stateful Load" "rsspp+pipeline,queue:Software Shared Queue" "rsspp+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --variables "QUEUE=[1-16]" --show-full --output --output-columns x raw --graph-filename drop-kthmorningquad-fw/.pdf --tags kthmorningquad  --graph-size 6 3.5 --config n_runs=3 --variables TIMING=0 --tags fw --result-path ".npf_results" --variables W=0 FREQ=1000 FW_CHKSUM=0  ${NPF_FLAGS}

test_fw_100:
	 ${NPF_PATH}npf-compare.py "rsspp+pianorss,DBACTIVE=0:RSS" rsspp+sprayer:Sprayer "rsspp+pipeline,queue:Software Shared Queue" "rsspp+pipeline,rr:Software RR Queue" "rsspp+pipeline,flowrr:Software Stateful RR" "rsspp+pipeline,flowrr,AWARE=1:Software Stateful Load" "rsspp+pipeline,queue:Software Shared Queue" "rsspp+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --variables "QUEUE=[1-16]" --show-full --output --output-columns x raw --graph-filename drop-kthmorningquad-fw/.pdf --tags kthmorningquad  --graph-size 6 3.5 --config n_runs=3 --variables TIMING=0 --tags fw --result-path ".npf_results" ${NPF_FLAGS} --tags replay --variables W=0 SAMPLE=100 GEN_BLOCKING=1 PKTGEN_REPLAY_TIME=20 LIMIT_TIME=20 FW_CHKSUM=false IGNORE=5 --output --output-columns x all --config n_runs=3 var_sync="{}" --tags nolat
