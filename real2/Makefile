include ../includes/Makefile.include

.NOTPARALLEL:

all: test graph

graph: plot.py
	python3 plot.py

COMMON=--tags replay --variables W=0 SAMPLE=100 GEN_BLOCKING=1 PKTGEN_REPLAY_TIME=10 LIMIT_TIME=10 TIMING=0 FW_CHKSUM=false IGNORE=5 --output --output-columns x all --config n_runs=3 var_sync="{}" --variables "QUEUE=[1-16]" --tags nolat

test_fw_only:
	${NPF_PATH}/npf-compare.py "rsspp+pianorss,fw,DBACTIVE=false:RSS" "rsspp+sprayer,fw:Sprayer" "rsspp+pianorss,fw:RSSPP" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} dut=${NPF_SERVER} --show-full --graph-filename real2-kthmorning-cx5/.pdf --tags promisc --tags kthmorningquad ${COMMON} ${NPF_FLAGS}

test_nat_only:
	${NPF_PATH}/npf-compare.py "rsspp+pianorss,fw,nat:RSSPP FW+NAT" "rsspp+rss,fw,nat:RSS FW+NAT" "rsspp+sprayer,fw,nat,shared:Sprayer FW+NAT"  --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} dut=${NPF_SERVER} --show-full --graph-filename real2-kthmorning-cx5/.pdf --tags promisc --tags kthmorningquad ${COMMON} ${NPF_FLAGS}

test_nat_alone:
	${NPF_PATH}/npf-compare.py "rsspp+pianorss,nat:RSSPP NAT" "rsspp+rss,nat:RSS NAT" "rsspp+sprayer,nat,shared:Sprayer NAT"  --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} dut=${NPF_SERVER} --show-full --graph-filename real2-kthmorning-cx5-natalone/.pdf --tags promisc --tags kthmorningquad ${COMMON} ${NPF_FLAGS}

test_dpi_alone:
	${NPF_PATH}/npf-compare.py "rsspp+pianorss,dpi:RSSPP DPI" "rsspp+pianorss,DBACTIVE=false,dpi:RSS DPI" "rsspp+sprayer,dpi,shared:Sprayer DPI"  --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} dut=${NPF_SERVER} --show-full --graph-filename real2-kthmorning-cx5-dpialone/.pdf --tags promisc --tags kthmorningquad ${COMMON} ${NPF_FLAGS}

test_dpi_only:
	${NPF_PATH}/npf-compare.py "rsspp+pianorss,fw,nat,dpi,DBACTIVE=false:RSS FW+NAT+DPI" "rsspp+pianorss,fw,nat,dpi:RSSPP FW+NAT+DPI"  "rsspp+sprayer,fw,nat,shared,dpi:Sprayer FW+NAT+DPI"  --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} dut=${NPF_SERVER} --show-full --graph-filename real2-kthmorning-cx5/.pdf --tags promisc --tags kthmorningquad ${COMMON} ${NPF_FLAGS} 

test:
	${NPF_PATH}/npf-compare.py "rsspp+pianorss,fw,DBACTIVE=false:RSS" "rsspp+sprayer,fw:Sprayer FW" "rsspp+pianorss,fw:RSSPP FW" "rsspp+pianorss,fw,nat,DBACTIVE=false:RSS FW+NAT" "rsspp+sprayer,fw,nat,shared:Sprayer FW+NAT" "rsspp+pianorss,fw,nat:RSSPP FW+NAT" "rsspp+pianorss,fw,nat,dpi,DBACTIVE=false:RSS FW+NAT+DPI" "rsspp+sprayer,fw,nat,shared,dpi:Sprayer FW+NAT+DPI" "rsspp+pianorss,fw,nat,dpi:RSSPP FW+NAT+DPI" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} dut=${NPF_SERVER} --show-full --graph-filename real2-kthmorning-cx5/.pdf --tags promisc --tags kthmorningquad ${COMMON} ${NPF_FLAGS}


#Noreorder did not change much
#test_noreorder:
#	${NPF_PATH}/npf-compare.py  "rsspp+rss,fw:RSS FW" "rsspp+sprayer,fw:Sprayer FW" "rsspp+pianorss,fw:RSSPP FW" "rsspp+pianorss,fw,nat,DBACTIVE=false:RSS FW+NAT" "rsspp+sprayer,fw,nat,shared:Sprayer FW+NAT" "rsspp+pianorss,fw,nat:RSSPP FW+NAT" "rsspp+pianorss,fw,nat,dpi,noreorder,DBACTIVE=false:RSS FW+NAT+DPI" "rsspp+sprayer,fw,nat,shared,dpi,noreorder:Sprayer FW+NAT+DPI" "rsspp+pianorss,fw,nat,dpi,noreorder:RSSPP FW+NAT+DPI" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} dut=${NPF_SERVER} --show-full --graph-filename real2-kthmorning-cx5/.pdf --tags promisc --tags kthmorningquad ${COMMON} ${NPF_FLAGS}


#Sprayer FW+NAT and FW+NAT+DPI. Used to confirm the weird behavior is legit
#test_sprayer_stateful:
#	${NPF_PATH}/npf-compare.py "rsspp+sprayer,fw,nat,shared:Sprayer FW+NAT" "rsspp+sprayer,fw,nat,shared,dpi:Sprayer FW+NAT+DPI" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} dut=${NPF_SERVER} --show-full --graph-filename real2-kthmorning-cx5/.pdf --tags promisc --tags kthmorningquad ${COMMON} ${NPF_FLAGS}


test_hfw:
	${NPF_PATH}/npf-compare.py "rsspp+rss,fw,nat:RSS FW+NAT" "rsspp+sprayer,fw,nat,shared:Sprayer FW+NAT" "rsspp+pianorss,fw,nat:RSSPP FW+NAT" "rsspp+pianorss,fw,nat,dpi,DBACTIVE=false:RSS FW+NAT+DPI" "rsspp+sprayer,fw,nat,shared,dpi:Sprayer FW+NAT+DPI" "rsspp+pianorss,fw,nat,dpi:RSSPP FW+NAT+DPI" "rsspp+rss,fw:RSS FW" "rsspp+sprayer,fw:Sprayer FW" "rsspp+pianorss,fw:RSSPP FW" --testie ../dpdk.testie --cluster client=${NPF_CLIENT} p=${NPF_SERVER} server=${NPF_SERVER} dut=${NPF_SERVER} --show-full --graph-filename real2-kthmorning-cx5-hfw/.pdf --tags promisc --tags kthmorningquad hfw ${COMMON} ${NPF_FLAGS}
