// sudo /home/tom/workspace/fastclick/bin/click --dpdk -l 0-15 -- limit=20000000 iface=0000:17:00.0 /home/tom/workspace/metron-testbed/metron-blackbox-metron/load-imbalance/tx-pcap-transformed.click trace=/mnt/traces/caida-2018/dirAT/trace.pcap endAfter=0 forceLen=0

define(
	$srcMac         50:6b:4b:43:8a:da,    // rack5 - enp3s0f0
	$rawSrcMac      506b4b438ada,

	$dstMac         50:6b:4b:43:88:ca,    // rack6 - enp3s0f0
	$rawDstMac      506b4b4388ca,
)

fdIN :: FromDump($trace, STOP true, TIMING false);
tdIN :: ToDump($traceOUT, SNAPLEN 128, FORCE_TS true);

ProgressBar(fdIN.filepos, fdIN.filesize);


classifier :: Classifier(12/0800, -);
check :: CheckIPHeader(VERBOSE false);
encap :: EnsureEther(ETHERTYPE 0x0800, SRC $srcMac, DST $dstMac);
legit   :: AverageCounterMP(IGNORE 0);
dropped :: AverageCounterMP(IGNORE 0);

/**
 * TX
 */
fdIN[0]
	-> MarkMACHeader
    -> cl :: CheckLength(1900, EXTRA_LENGTH true)
    -> Unstrip($strip)
	-> MarkMACHeader
    -> Pad(RANDOM true)
//    -> Print(DATA, LENGTH 256)
	-> encap
//	-> Print(INP, CONTENTS HEX, MAXLENGTH 80)
	-> classifier;

classifier[0]
	-> Strip(14)
	-> SetIPChecksum()
	-> check
    -> ipc :: IPClassifier(proto tcp, proto udp, proto icmp, -)[0-3] =>
    protos :: { 
        input[0] -> tcp :: Counter()
        -> SetTCPChecksum 
        //-> stcp::Counter() 
        -> MoveData(SRC_OFFSET 36, DST_OFFSET -4, LENGTH 2) -> [0];
        input[1] -> udp :: Counter() 
        ->  SetUDPChecksum -> sudp::Counter() 
        -> MoveData(SRC_OFFSET 26, DST_OFFSET -4, LENGTH 2) -> [0];
        //ICMP and tunnels -> use IP header
        input[2] -> icmp :: Counter() -> MoveData(SRC_OFFSET 10, DST_OFFSET -4, LENGTH 2) -> [0];
        input[3] -> other :: Counter() -> MoveData(SRC_OFFSET 10, DST_OFFSET -4, LENGTH 2) -> [0];
    }
	-> Unstrip(14)
	-> legit
	-> tdIN;

cl[1] -> Print ->  cld :: CounterMP() -> Discard;
classifier[1] -> dropped;
check[1] -> dropped;
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
	print " Dropped by CheckLength: "$(cld.count),
	print " Dropped: "$(dropped.count),
	print "",
	print "Tx Trace: $(trace)",
	print "Tx Count: $(legit.count) packets",
	print "Tx  Rate: $(div $(legit.link_rate) 1000000000) Gbps",
	stop
);
