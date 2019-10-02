#!/bin/bash

source $(dirname "$0")/../includes/Makefile.include

files=$@
echo 0 > /tmp/cur
for file in files ; do
    i=$(cat /tmp/cur)
    echo $i
    echo "$(($i+1))" > /tmp/cur
    ${NPF_PATH}/npf/build/fastclick $(dirname "$0")/pcap-rewrite.click trace=$file traceOUT=${file}-rewriten.pcap prefix=$((130 + $i)).0.0.0/8' &
done
