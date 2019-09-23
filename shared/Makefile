all: plot

plot: plot.py
	python3 plot.py

test:
	~/npf/npf-compare.py "metron+rss,wpf,nowpf:RSS" "metron+sprayer,nowpf,wpf:Sprayer" "metron+rss,wpf:RSS" "metron+sprayer,wpf:Sprayer" "metron+rss,wpf,wpf_pwrite:RSS" "metron+sprayer,wpf,wpf_pwrite:Sprayer" "metron+rss,wpf,wpf_seq,wpf_pwrite:RSS" "metron+sprayer,wpf,wpf_seq,wpf_pwrite:Sprayer" --testie ../dpdk.testie --cluster client=nslrack12-100G,nic=1 p=nslrack14-100G,nic=0 server=nslrack14-100G,nic=0 dut=nslrack14-100G,nic=0 --show-full --graph-filename ~/workspace/rss-experiments/shared/shared-udp-cx5.pdf --tags promisc --variables ITERATION_TIME=1 TIMING=1 --no-build --no-build-deps fastclick --graph-size 6 2.2 --config n_runs=1 "graph_variables_as_series={WPF,SERIE}" --max-results --output --output-columns x all --graph-group-repo --variables BURST=1 RX_VEC_EN=0 "QUEUE=8" --config n_runs=3 "graph_color={1,2}" --variables GEN_LENGTH=1500 TIMING=0 RATE=2000000 advertise=0 LIMIT=3000000 GEN_REPLAY=1 "GEN_FLOWS=[1*1024]" "GEN_BURST=1000" W=0 CHECKORDER=1 --tags udp rate --config n_runs=3 --build-folder ~/npf/build/
