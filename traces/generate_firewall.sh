#!/bin/bash


if [ $# -ne 3 ] ; then
    echo "Syntax error. Got only $# arguments"
    echo "Usage : $0 trace_in rulesMax rules_out"
    exit 1
fi 

IN=$1
rulesMax=$2
OUT=$3

echo "Will set the end of destination MAC addresses from checksum in $IN to $OUT, randomly filling payload before computing checksum then snapping the packets to 128 bytes. It is the responsability of the replayer to fix checksum again."
source $(dirname "$0")/../includes/Makefile.include
${NPF_PATH}/build/rsspp/bin/click limit=20000000 $(dirname "$0")/gen-ip-filter.click trace=$IN endAfter=0 forceLen=0 strip=0 rulesFile=$OUT rulesNb=$rulesMax
sed -i 's/,$//g' $OUT
