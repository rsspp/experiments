/**
 * Generate IPFilter rules out of a trace.
 */

// sudo ~/nfv/fastclick/bin/click --dpdk -l 0-15  --socket-mem 62,2 --huge-dir /mnt/hugepages -v -- gen-ip-filter.click rulesNb=800 pattern=IPFILTER

////////////////////////////////////////////////////////////
// Testbed configuration
////////////////////////////////////////////////////////////
define(
	$inSrcMac    ae:aa:aa:65:dd:2b,
	$inDstMac    ae:aa:aa:02:27:a6,

	$ignore      0,
	$rulesNb     1000,
	$pattern     IPFILTER,
	$trace       /mnt/traces/uliege/INfull_64.pcap,
	$prefix      24,
	$forceIp     true,
	$endAfter    0,
	$rulesFile   rules
);

d :: DPDKInfo(NB_SOCKET_MBUF 14008256, NB_SOCKET_MBUF 8192);

fdIN :: FromDump($trace, STOP true, TIMING false, FORCE_IP $forceIp, FORCE_LEN 0, END_AFTER $endAfter);

fdIN
	-> EnsureEther(0x0800, SRC $inSrcMac, DST $inDstMac)
	-> all :: AverageCounterMP(IGNORE $ignore)
	-> classifier :: Classifier(12/0800, -)
	-> Strip(14)
	-> SetIPChecksum()
	-> check :: CheckIPHeader(VERBOSE false)
//	-> IPPrint(LENGTH true, TTL true)
	-> gen :: GenerateIPFilter(NB_RULES $rulesNb, PATTERN_TYPE $pattern, KEEP_SPORT false, KEEP_DPORT false, PREFIX $prefix)
	-> goodIp :: AverageCounterMP(IGNORE $ignore)
	-> Discard;

classifier[1] -> nonIp :: AverageCounterMP -> Discard;
check[1] -> badIp :: AverageCounterMP -> Discard;

DriverManager(
	pause,
	set loss $(sub 100 $(mul $(div $(goodIp.count) $(all.count)) 100)),
	set dropped $(add $(badIp.count) $(nonIp.count)),
	print "Finished with $(all.count) input packets",
	print "",
	print "Non-IPv4 packets: "$(nonIp.count),
	print "Bad-IPv4 packets: "$(badIp.count),
	print " Dropped packets: "$dropped,
	print "",
	print "    IPv4 packets: "$(goodIp.count)" out of "$(all.count)" ("$loss"% dropped)",
	print "",
	print "Dumping rules to file: "$rulesFile,
	print > $rulesFile $(gen.dump),
	print "",
	print "RESULT-PKT-COUNT "$(goodIp.count),
	print "RESULT-PKT-DROP "$dropped,
	print "RESULT-RULE-COUNT "$(gen.rules_nb),
	stop
);
