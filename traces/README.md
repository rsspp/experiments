transform.sh
------------

Usage: transform.sh original\_trace.pcap destination\_trace.pcap

Will pad packets with random payload, recompute checksum, copy the checksum to the end of the destination mac address, and then write the packets in destination\_trace snapped to 128bytes. Therefore the checksum will not be good anymore, so the generator fix it again.
This is needed to simulate Sprayer, as dispatching packets using the checksum is fairly complex (probably impossible with CX5) but, dispatching packets to core according to a mask of the destination mac address is quite easy.

parallel combination of traces
------------------------------
To combine multiple traces together in parallel (we consider all of their first packets to start at time 0), rewriting flows along the way to prevent collisions. This is how the campus #4 was made. You may use tracesplit to split a huge trace in 90 seconds windows as follow :
tracesplit -i 90 pcapfile:20190507.morning.merged.ip.anon.pcap pcapfile:splits/20190507.morning.merged.ip.anon.pcap   

Then rewrite each trace to have flow in a unique prefix:
parallel.sh splits/2019....XXXX.pcap spltis/2019....YYYY.pcap [...]

Then merge the windows with:
mergecap -F pcap -w DESTINATION.pcap splits/2019....XXXX-rewriten.pcap  splits/2019.....YYYYY-rewriten.pcap
