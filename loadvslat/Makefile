include ../includes/Makefile.include

.NOTPARALLEL:

all: graph test

test: loadvsdrop loadvslat loadvslatcdf

graph: graphloadvslat graphloadvsdrop

graphloadvslat:
	python3 plotvslat.py

graphloadvsdrop:
	python3 plotvsdrop.py

loadvslat:
	${NPF_PATH}npf-compare.py "rsspp+rss:RSS" "rsspp+pianorss,BALANCE_PERIOD=100:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --graph-filename ./loadvslat-kthmorning-cx5/.pdf --output --output-columns x all --tags kthmorningquad --graph-size 7 4.5 --variables BVERBOSE=0 QUEUE=4 AUTOSCALE=0 "W=400" TIMING="[90-170#5]" SAMPLE=100 ITERATION_TIME=1 --tags nolatlog promisc replay dump --graph-size 6 3 --config "var_log+={LAT}" n_runs=3 ${NPF_FLAGS}

loadvslatcdf:
	#Exactlythe same test, just do for 105,125,135
	${NPF_PATH}npf-compare.py "rsspp+rss:RSS" "rsspp+pianorss,BALANCE_PERIOD=100:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --graph-filename ./loadvslatcdf-kthmorning-cx5/.pdf --output --tags kthmorningquad --graph-size 7 4.5 --max-results --variables BVERBOSE=0 QUEUE=4 AUTOSCALE=0 "W=400" TIMING="{105,125,135}" SAMPLE=100 ITERATION_TIME=1 --tags nolatlog promisc replay dump --graph-size 6 3 --config "var_log+={LAT}" n_runs=1 ${NPF_FLAGS}

loadvsdrop:
	#Basicallythe same test but in iterative mode, so we get IDROPPED every seconds
	#Weneed to do the test twice because iterative mode resets latency every seconds, the previous test wants to observer the whole latency
	${NPF_PATH}npf-compare.py "rsspp+rss:RSS" "rsspp+pianorss,BALANCE_PERIOD=100:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --graph-filename ./loadvsdrop-kthmorning-cx5/.pdf --output --tags kthmorningquad --graph-size 6 4.5 --config n_runs=3 --variables BVERBOSE=0 QUEUE=4 AUTOSCALE=0 "W=400" TIMING_FNT_BASE="{120,130,140}" SAMPLE=100 ITERATION_TIME=1 TIMING=1 --tags nolatlog promisc fnt --output-columns x all --config "graph_variables_as_series={TIMING_FNT_BASE}" ${NPF_FLAGS}
