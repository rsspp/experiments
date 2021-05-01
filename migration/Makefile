include ../includes/Makefile.include

.NOTPARALLEL:

all: test graph

graph: plot.py
	python3 plot.py

test:
	${NPF_PATH}npf-compare.py "rsspp+dynamicrss:Group-table" "rsspp+dynamicrss,shared:Shared" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --show-full --graph-filename migration-udp-cx5/.pdf --tags promisc --variables ITERATION_TIME=0.2 --graph-size 6 2.2 --config "graph_variables_as_series={WPF,SERIE}" --output --output-columns x all --variables "QUEUE=15" --variables GEN_LENGTH=1500 TIMING=0 advertise=0 LIMIT=2000000 GEN_REPLAY=40 "GEN_FLOWS=256" "GEN_BURST=1000" W=100 STARTCPU=1 REPORT_PERIOD=0.2 --tags udp migration checkorder --config n_runs=1 ${NPF_FLAGS}
#	//pqos
