all: plot

plot: plot.py
	python3 plot.py

quad:
	cd ~/npf && ./npf-compare.py metron+rss:RSS metron+sprayer:Sprayer "metron+pipeline,queue:Software Shared Queue" "metron+pipeline,rr:Software RR Queue" "metron+pipeline,flowrr:Software Stateful RR" "metron+pipeline,flowrr,AWARE=1:Software Stateful Load" "metron+staticmetron:Metron Static" "metron+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=nslrack12-100G,nic=1 p=nslrack14-100G,nic=0 server=nslrack14-100G,nic=0 dut=nslrack14-100G,nic=0 --output --output-columns x raw  --graph-filename ~/workspace/rss-experiments/imbalance/imbalance-kthmorningquad  --no-build --config n_runs=1 --variables TIMING=1 QUEUE=8 W=150 --tags kthmorningquad fnt --max-results

single:
	cd ~/npf && ./npf-compare.py metron+rss:RSS metron+sprayer:Sprayer "metron+pipeline,queue:Software Shared Queue" "metron+pipeline,rr:Software RR Queue" "metron+pipeline,flowrr:Software Stateful RR" "metron+pipeline,flowrr,AWARE=1:Software Stateful Load" "metron+staticmetron:Metron Static" "metron+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=nslrack12-100G,nic=1 p=nslrack14-100G,nic=0 server=nslrack14-100G,nic=0 dut=nslrack14-100G,nic=0 --output --output-columns x raw  --graph-filename ~/workspace/rss-experiments/imbalance/imbalance-kthmorningsingle  --no-build --config n_runs=1 --variables TIMING=1 QUEUE=8 W=500 --tags kthmorningsingle fnt --max-results

caida:
	cd ~/npf && ./npf-compare.py metron+rss:RSS metron+sprayer:Sprayer "metron+pipeline,queue:Software Shared Queue" "metron+pipeline,rr:Software RR Queue" "metron+pipeline,flowrr:Software Stateful RR" "metron+pipeline,flowrr,AWARE=1:Software Stateful Load" "metron+staticmetron:Metron Static" "metron+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=nslrack12-100G,nic=1 p=nslrack14-100G,nic=0 server=nslrack14-100G,nic=0 dut=nslrack14-100G,nic=0 --output --output-columns x raw  --graph-filename ~/workspace/rss-experiments/imbalance/imbalance-caida18  --no-build --config n_runs=1 --variables TIMING=1 QUEUE=8 W=1000 --tags caida18 fnt --max-results

testie: caida single quad

.NOTPARALLEL:

allquad:
	~/npf/npf-compare.py "metron+rss:RSS" metron+sprayer:Sprayer "metron+pipeline,queue:Software Shared Queue" "metron+pipeline,rr:Software RR Queue" "metron+pipeline,flowrr:Software Stateful RR" "metron+pipeline,flowrr,AWARE=1:Software Stateful Load" "metron+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=nslrack12-100G,nic=1 p=nslrack14-100G,nic=0 server=nslrack14-100G,nic=0 --variables "QUEUE=[1-16]" --show-full --output --output-columns x raw --graph-filename ~/workspace/rss-experiments/imbalance/imbalance-all-kthmorningquad.pdf --tags kthmorningquad --no-build --graph-size 6 3.5 --config "graph_y_group={result:all}" n_runs=3 --variables TIMING=1 WBASE=150 --tags fnt dynaw --no-graph --result-path ".npf_results" --build-folder ~/npf/build/ --max-results


allcaida:
	~/npf/npf-compare.py "metron+rss:RSS" metron+sprayer:Sprayer "metron+pipeline,queue:Software Shared Queue" "metron+pipeline,rr:Software RR Queue" "metron+pipeline,flowrr:Software Stateful RR" "metron+pipeline,flowrr,AWARE=1:Software Stateful Load" "metron+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=nslrack12-100G,nic=1 p=nslrack14-100G,nic=0 server=nslrack14-100G,nic=0 --variables "QUEUE=[1-16]" --show-full --output --output-columns x raw --graph-filename ~/workspace/rss-experiments/imbalance/imbalance-all-caida18.pdf --tags caida18 --no-build --graph-size 6 3.5 --config "graph_y_group={result:all}" n_runs=3 --variables TIMING=1 WBASE=500 --tags fnt dynaw --no-graph --result-path ".npf_results_caida18" --build-folder ~/npf/build/ --max-results

allsingle:
	~/npf/npf-compare.py "metron+rss:RSS" metron+sprayer:Sprayer "metron+pipeline,queue:Software Shared Queue" "metron+pipeline,rr:Software RR Queue" "metron+pipeline,flowrr:Software Stateful RR" "metron+pipeline,flowrr,AWARE=1:Software Stateful Load" "metron+dynamicmetron:Metron Dynamic" "rsspp+pianorss:RSSPP" --testie ../dpdk.testie --cluster client=nslrack12-100G,nic=1 p=nslrack14-100G,nic=0 server=nslrack14-100G,nic=0 --variables "QUEUE=[1-16]" --show-full --output --output-columns x raw --graph-filename ~/workspace/rss-experiments/imbalance/imbalance-all-kthmorningsingle.pdf --tags kthmorningsingle --no-build --graph-size 6 3.5 --config "graph_y_group={result:all}" n_runs=3 --variables TIMING=1 WBASE=1000 --tags fnt dynaw --no-graph --result-path ".npf_results_kthmorningsingle" --build-folder ~/npf/build/ --max-results

testall: allsingle allcaida allquad
