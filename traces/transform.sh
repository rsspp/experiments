#!/bin/bash


if [ $# -ne 2 ] ; then
    echo "Syntax error. Got only $# arguments"
    echo "Usage : $0 trace_in trace_out"
    exit 1
fi 

IN=$1
OUT=$2

echo "Will set the end of destination MAC addresses from checksum in $IN to $OUT, randomly filling payload before computing checksum then snapping the packets to 128 bytes. It is the responsability of the replayer to fix checksum again."
source $(dirname "$0")/../includes/Makefile.include
${NPF_PATH}build/fastclick/bin/click limit=20000000 $(dirname "$0")/pcap-transform.click trace=$IN endAfter=0 forceLen=0 strip=0 traceOUT=$OUT
