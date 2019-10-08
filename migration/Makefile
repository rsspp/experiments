all: plot

graph: plot.py
	python3 plot.py

testie:
	${NPF_PATH}/npf-compare.py "rsspp+dynamicrss:Group-table" "rsspp+dynamicrss,shared:Shared" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} dut=${NPF_SERVER} --show-full --graph-filename ./migration/migration-udp-rate-cx5.pdf --tags promisc --variables ITERATION_TIME=0.2 --graph-size 6 2.2 --config n_runs=1 "graph_variables_as_series={WPF,SERIE}" --output --output-columns x all --variables "QUEUE=15" --config n_runs=3 "graph_color={1,2}" --variables GEN_LENGTH=1500 TIMING=0 advertise=0 LIMIT=2000000 GEN_REPLAY=40 "GEN_FLOWS=256" "GEN_BURST=1000" W=100 STARTCPU=1 REPORT_PERIOD=0.2 --tags udp migration pqos checkorder rate --variables GEN_RATE=1000000 --config n_runs=1 $NPF_FLAGS
