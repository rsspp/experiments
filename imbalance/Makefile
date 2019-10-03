include ../includes/Makefile.include

.NOTPARALLEL:

all: testie testall plot


plot: plot.py
	python3 plot.py

quad:
	${NPF_PATH}/npf-compare.py rsspp+rss:RSS rsspp+sprayer:Sprayer "rsspp+pipeline,queue:Software Shared Queue" "rsspp+pipeline,rr:Software RR Queue" "rsspp+pipeline,flowrr:Software Stateful RR" "rsspp+pipeline,flowrr,AWARE=1:Software Stateful Load" "rsspp+staticmetron:Metron Static" "rsspp+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} dut=nslrack14-100G,nic=0 --output --output-columns x raw  --graph-filename ./imbalance/imbalance-kthmorningquad  --no-build --config n_runs=1 --variables TIMING=1 QUEUE=8 W=150 --tags kthmorningquad fnt --max-results


single:
	${NPF_PATH}/npf-compare.py rsspp+rss:RSS rsspp+sprayer:Sprayer "rsspp+pipeline,queue:Software Shared Queue" "rsspp+pipeline,rr:Software RR Queue" "rsspp+pipeline,flowrr:Software Stateful RR" "rsspp+pipeline,flowrr,AWARE=1:Software Stateful Load" "rsspp+staticmetron:Metron Static" "rsspp+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} dut=nslrack14-100G,nic=0 --output --output-columns x raw  --graph-filename ./imbalance/imbalance-kthmorningsingle  --no-build --config n_runs=1 --variables TIMING=1 QUEUE=8 W=500 --tags kthmorningsingle fnt --max-results

caida:
    ${NPF_PATH}/npf-compare.py rsspp+rss:RSS rsspp+sprayer:Sprayer "rsspp+pipeline,queue:Software Shared Queue" "rsspp+pipeline,rr:Software RR Queue" "rsspp+pipeline,flowrr:Software Stateful RR" "rsspp+pipeline,flowrr,AWARE=1:Software Stateful Load" "rsspp+staticmetron:Metron Static" "rsspp+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} dut=nslrack14-100G,nic=0 --output --output-columns x raw  --graph-filename ./imbalance/imbalance-caida18  --no-build --config n_runs=1 --variables TIMING=1 QUEUE=8 W=1000 --tags caida18 fnt --max-results

testie: single quad
#caida


allquad:
	 ${NPF_PATH}/npf-compare.py "rsspp+rss:RSS" rsspp+sprayer:Sprayer "rsspp+pipeline,queue:Software Shared Queue" "rsspp+pipeline,rr:Software RR Queue" "rsspp+pipeline,flowrr:Software Stateful RR" "rsspp+pipeline,flowrr,AWARE=1:Software Stateful Load" "rsspp+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} --variables "QUEUE=[1-16]" --show-full --output --output-columns x raw --graph-filename ./imbalance/imbalance-all-kthmorningquad.pdf --tags kthmorningquad --no-build --graph-size 6 3.5 --config "graph_y_group={result:all}" n_runs=3 --variables TIMING=1 WBASE=150 --tags fnt dynaw --no-graph --result-path ".npf_results"  --max-results


allcaida:
	 ${NPF_PATH}/npf-compare.py "rsspp+rss:RSS" rsspp+sprayer:Sprayer "rsspp+pipeline,queue:Software Shared Queue" "rsspp+pipeline,rr:Software RR Queue" "rsspp+pipeline,flowrr:Software Stateful RR" "rsspp+pipeline,flowrr,AWARE=1:Software Stateful Load" "rsspp+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} --variables "QUEUE=[1-16]" --show-full --output --output-columns x raw --graph-filename ./imbalance/imbalance-all-caida18.pdf --tags caida18 --no-build --graph-size 6 3.5 --config "graph_y_group={result:all}" n_runs=3 --variables TIMING=1 WBASE=500 --tags fnt dynaw --no-graph --result-path ".npf_results_caida18"  --max-results

allsingle:
	 ${NPF_PATH}/npf-compare.py "rsspp+rss:RSS" rsspp+sprayer:Sprayer "rsspp+pipeline,queue:Software Shared Queue" "rsspp+pipeline,rr:Software RR Queue" "rsspp+pipeline,flowrr:Software Stateful RR" "rsspp+pipeline,flowrr,AWARE=1:Software Stateful Load" "rsspp+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} --variables "QUEUE=[1-16]" --show-full --output --output-columns x raw --graph-filename ./imbalance/imbalance-all-kthmorningsingle.pdf --tags kthmorningsingle --no-build --graph-size 6 3.5 --config "graph_y_group={result:all}" n_runs=3 --variables TIMING=1 WBASE=1000 --tags fnt dynaw --no-graph --result-path ".npf_results_kthmorningsingle" --max-results

testall: allsingle allquad
#allcaida
