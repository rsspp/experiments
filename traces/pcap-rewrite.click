// sudo /home/tom/workspace/fastclick/bin/click --dpdk -l 0-15 -- limit=20000000 iface=0000:17:00.0 /home/tom/workspace/metron-testbed/metron-blackbox-metron/load-imbalance/tx-pcap-transformed.click trace=/mnt/traces/caida-2018/dirAT/trace.pcap endAfter=0 forceLen=0

classifier :: Classifier(12/0800, -);
legit   :: AverageCounterMP(IGNORE 0);
dropped :: AverageCounterMP(IGNORE 0);

fdIN :: FromDump($trace, STOP true, TIMING false);
tdIN :: ToDump($traceOUT, SNAPLEN 128, FORCE_TS true);

fdIN
	-> MarkMACHeader
    -> SetTimestampDelta
	-> classifier;

classifier[0]
	-> Strip(14)
	-> MarkIPHeader
    -> IPAddrRewriter(pattern $prefix - 0 0)
	-> Unstrip(14)
	-> legit
	-> tdIN;

classifier[1] -> dropped;
dropped -> Discard;

DriverManager(
	pause,
	print "EVENT GEN_STOPPED",
	print "",
    print "        TCP: $(protos/tcp.count) ($(protos/stcp.count) non malformed dropped)",
    print "        UDP: $(protos/udp.count) ($(protos/sudp.count) non malformed dropped)",
    print "       ICMP: "$(protos/icmp.count),
    print "      Other: "$(protos/other.count),
	print "       IPv4: "$(legit.count),
	print " Dropped by Classifier: "$(sub $(dropped.count) $(check.drops)),
	print " Dropped by CheckIPHeader: "$(check.drops),
	print " Dropped: "$(dropped.count),
	print "",
	print "Tx Trace: $(trace)",
	print "Tx Count: $(legit.count) packets",
	print "Tx  Rate: $(div $(legit.link_rate) 1000000000) Gbps",
	stop
);