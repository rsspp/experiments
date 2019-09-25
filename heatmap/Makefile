include ../includes/Makefile.include

.NOTPARALLEL:

all: test graph

graph:
	python3 plot.py

#We run the test once for CPU load, and 3 times for RTT and bandwidth

test: test_cpu test_rtt

test_cpu:
	${NPF_PATH}/npf-run.py rsspp --testie ../kernel.testie --show-full --show-cmd --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --output --graph-filename results/ --output-columns x raw ${NPF_FLAGS} --no-graph

test_rtt:
	${NPF_PATH}/npf-run.py rsspp --testie ../kernel.testie --show-full --show-cmd --cluster client=${NPF_CLIENT} server=${NPF_SERVER} --output --graph-filename results-3/ --output-columns x raw ${NPF_FLAGS} --config n_runs=1 --no-graph

arch=$(shell date '+%Y%m%d')

clean:
	mkdir -p archives/${arch}/results
	mkdir -p archives/${arch}/results-3
	mv *.pdf archives/${arch}
	mv results/* archives/${arch}/results
	mv results-3/* archives/${arch}/results-3
