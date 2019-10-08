Transformation of traces for Sprayer emulation (transform.sh)
-------------------------------------------------------------
To emulate Sprayer, as dispatching packets using the checksum is fairly complex (probably impossible with Mellanox ConnectX 5 NICs), we program the server nic to dispatch packets to core according to a mask of the source mac address. Therefore the trace needs to be modified to copy the checksum at the end of the source mac address.

Usage: transform.sh original\_trace.pcap destination\_trace.pcap

The script will pad packets with random payload, recompute checksum, copy the checksum to the end of the source mac address, and then write the packets in destination\_trace snapped to 128bytes. Therefore the checksum will not be good anymore, so the generator has to fix it again.

Parallel combination of traces
------------------------------
To combine multiple traces together in parallel (we consider all of their first packets to start at time 0), rewriting flows along the way to prevent collisions. This is how the campus #4 was made. 

First, use tracesplit to split a huge trace in 90 seconds windows as follow :
tracesplit -i 90 pcapfile:bigtrace.pcap pcapfile:splits/smalltrace.pcap   

Then rewrite each trace to have flow in a unique prefix:
parallel.sh splits/smalltrace.XXXX.pcap spltis/smalltrace.YYYY.pcap [...]

Then merge the windows with:
mergecap -F pcap -w DESTINATION.pcap splits/smalltrace.XXXX-rewriten.pcap  splits/smalltrace-rewriten.pcap
