include ../includes/Makefile.include

METHODS=rsspp+rss:RSS rsspp+sprayer:Sprayer "rsspp+pipeline,queue:Software Shared Queue" "rsspp+pipeline,rr:Software RR Queue" "rsspp+pipeline,flowrr:Software Stateful RR" "rsspp+pipeline,flowrr,AWARE=1:Software Stateful Load"
METHODS+="rsspp+staticmetron:Metron Static" "rsspp+dynamicmetron:Metron Dynamic"
METHODS+="rsspp+pianorss:RSSPP"

.NOTPARALLEL:

all: testie testall plot


graph: plot.py
	python3 plot.py

quad:
	${NPF_PATH}npf-compare.py ${METHODS} --testie ../dpdk.testie --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --output --output-columns x raw  --graph-filename ./imbalance/imbalance-kthmorningquad  ${NPF_FLAGS} --config n_runs=1 --variables TIMING=1 QUEUE=8 W=150 --tags kthmorningquad fnt --max-results ${NPF_FLAGS}


single:
	${NPF_PATH}npf-compare.py ${METHODS} --testie ../dpdk.testie --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --output --output-columns x raw  --graph-filename ./imbalance/imbalance-kthmorningsingle  ${NPF_FLAGS} --config n_runs=1 --variables TIMING=1 QUEUE=8 W=500 --tags kthmorningsingle fnt --max-results ${NPF_FLAGS}

caida:
	${NPF_PATH}npf-compare.py ${METHODS} --testie ../dpdk.testie --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --output --output-columns x raw  --graph-filename ./imbalance/imbalance-caida18  ${NPF_FLAGS} --config n_runs=1 --variables TIMING=1 QUEUE=8 W=1000 --tags caida18 fnt --max-results ${NPF_FLAGS}

testie: single quad
#caida


allquad:
	 ${NPF_PATH}npf-compare.py "rsspp+rss:RSS" rsspp+sprayer:Sprayer "rsspp+pipeline,queue:Software Shared Queue" "rsspp+pipeline,rr:Software RR Queue" "rsspp+pipeline,flowrr:Software Stateful RR" "rsspp+pipeline,flowrr,AWARE=1:Software Stateful Load" "rsspp+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --variables "QUEUE=[1-16]" --show-full --output --output-columns x raw --graph-filename ./imbalance/imbalance-all-kthmorningquad.pdf --tags kthmorningquad ${NPF_FLAGS} --graph-size 6 3.5 --config "graph_y_groun_runs=3 --variables TIMING=1 WBASE=150 --tags fnt dynaw --no-graph --result-path ".npf_results"  --max-results ${NPF_FLAGS}


allcaida:
	 ${NPF_PATH}npf-compare.py "rsspp+rss:RSS" rsspp+sprayer:Sprayer "rsspp+pipeline,queue:Software Shared Queue" "rsspp+pipeline,rr:Software RR Queue" "rsspp+pipeline,flowrr:Software Stateful RR" "rsspp+pipeline,flowrr,AWARE=1:Software Stateful Load" "rsspp+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --variables "QUEUE=[1-16]" --show-full --output --output-columns x raw --graph-filename ./imbalance/imbalance-all-caida18.pdf --tags caida18 ${NPF_FLAGS} --graph-size 6 3.5 --config "graph_y_groun_runs=3 --variables TIMING=1 WBASE=500 --tags fnt dynaw --no-graph --result-path ".npf_results_caida18"  --max-results ${NPF_FLAGS}

allsingle:
	 ${NPF_PATH}npf-compare.py "rsspp+rss:RSS" rsspp+sprayer:Sprayer "rsspp+pipeline,queue:Software Shared Queue" "rsspp+pipeline,rr:Software RR Queue" "rsspp+pipeline,flowrr:Software Stateful RR" "rsspp+pipeline,flowrr,AWARE=1:Software Stateful Load" "rsspp+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --variables "QUEUE=[1-16]" --show-full --output --output-columns x raw --graph-filename ./imbalance/imbalance-all-kthmorningsingle.pdf --tags kthmorningsingle ${NPF_FLAGS} --graph-size 6 3.5 --config "graph_y_groun_runs=3 --variables TIMING=1 WBASE=1000 --tags fnt dynaw --no-graph --result-path ".npf_results_kthmorningsingle" --max-results ${NPF_FLAGS}

testall: allsingle allquad
#allcaida
