
include ../includes/Makefile.include

all: graph test


test: loadvsdrop loadvslat

graph:
	python3 plot.py



loadvslat:
	${NPF_PATH}/npf-compare.py "metron+rss:RSS" "rsspp+pianorss,BALANCE_PERIOD=100:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} --show-full --graph-filename ./loadvslat-kthmorning-cx5.pdf --output --tags kthmorningquad --graph-size 7 4.5 --variables BVERBOSE=0 --max-results --variables BVERBOSE=0 QUEUE=4 AUTOSCALE=0 "W=400" TIMING="[100-160#10]" SAMPLE=100 --tags nolatlog promisc replay dump --graph-size 6 3 --config "var_log+={LAT}" n_runs=1 ${NPF_FLAGS}	

loadvsdrop:
	echo "Load vs drop data is now taken from loadvslat"
#	${NPF_PATH}/npf-compare.py "metron+rss:RSS" "rsspp+pianorss,BALANCE_PERIOD=100:RSSPP" --testie ../dpdk.testie --cluster client=nslrack12-100G,nic=1 p=nslrack14-100G,nic=0 server=nslrack14-100G,nic=0 --show-full --graph-filename ~/workspace/rss-experiments/loadvslat/loadvsdrop-kthmorning-cx5.pdf --output --tags kthmorningquad --graph-size 6 4.5 --config n_runs=3 --variables BVERBOSE=0 --no-build-deps fastclick --max-results --variables BVERBOSE=0 QUEUE=4 AUTOSCALE=0 "W=400" TIMING_FNT_BASE="[120-145#5]" SAMPLE=100 ITERATION_TIME=1 --tags fnt nolatlog promisc --graph-size 6 2 --output-columns x all --config "graph_variables_as_series={TIMING_FNT_BASE}" "graph_color={1,2}" --use-last 1 --variables TIMING=1 --config "var_lim={}" --config "graph_labels={RSS - 120%,RSS - 125%,RSS - 130%,RSS - 135%,RSS - 140%,RSS - 145%,RSS++ - 120%,RSS++ - 125%,RSS++ - 130%,RSS++ - 135%,RSS++ - 140%,RSS++ - 145%}" "legend_loc=outer center" "legend_ncol=4" "legend_bbox={0,1,1,.15}" "var_names+={IGDROPPED:KPackets dropped}"
