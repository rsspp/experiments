include ../includes/Makefile.include

.NOTPARALLEL:

all: test graph

graph:plot.py
	python3 plot.py

test:
	 ${NPF_PATH}/npf-compare.py "rsspp+rss,wpf,nowpf:RSS" "rsspp+sprayer,nowpf,wpf:Sprayer" "rsspp+rss,wpf:RSS" "rsspp+sprayer,wpf:Sprayer" "rsspp+rss,wpf,wpf_pwrite:RSS" "rsspp+sprayer,wpf,wpf_pwrite:Sprayer" "rsspp+rss,wpf,wpf_seq,wpf_pwrite:RSS" "rsspp+sprayer,wpf,wpf_seq,wpf_pwrite:Sprayer" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} dut=${NPF_SERVER} --show-full --graph-filename shared-udp-cx5/.pdf --tags promisc --variables ITERATION_TIME=1 --graph-size 6 2.2 --config n_runs=1 "graph_variables_as_series={WPF,SERIE}" --output --output-columns x all --graph-group-repo --variables BURST=1 RX_VEC_EN=0 "QUEUE=8" --config n_runs=3 "graph_color={1,2}" --variables GEN_LENGTH=1500 TIMING=0 RATE=2000000 advertise=0 LIMIT=3000000 GEN_REPLAY=1 "GEN_FLOWS=[1*1024]" "GEN_BURST=1000" W=0 CHECKORDER=1 --tags udp rate --config n_runs=3 ${NPF_FLAGS}
