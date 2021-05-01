include ../includes/Makefile.include

.NOTPARALLEL:

all: test graph


graph:
	python3 plot.py

test: test_diff test_nodiff

test_diff:
	${NPF_PATH}npf-compare.py "rsspp+pipeline,kthmorningsingle:Campus" "rsspp+pipeline,kthmorningquad:Campus #4" --testie ../pcap-counter.testie --cluster client=${NPF_CLIENT} --output --graph-filename iter-count-diff/.pdf --graph-size 6 2.8 --tags count promisc ffnt --variables TIMING=1 ${NPF_FLAGS}

test_nodiff:
	${NPF_PATH}npf-compare.py "rsspp+pipeline,kthmorningsingle:Campus" "rsspp+pipeline,kthmorningquad:Campus #4" --testie ../pcap-counter.testie --cluster client=${NPF_CLIENT} --output --graph-filename iter-count-nodiff/.pdf --graph-size 6 2.8 --tags count promisc ffnt --variables TIMING=1 DIFFERENTIAL=False ${NPF_FLAGS}


