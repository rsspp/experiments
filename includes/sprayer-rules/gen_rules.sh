#!/bin/bash
for i in $(seq 1 32) ; do
    rm rules-256-${i}queue
    vim -c ":for i in range(0,255) | put ='flow create 0 ingress pattern eth src spec 00:00:00:00:00:'.printf('%02x',i).' src mask 00:00:00:00:00:ff / end actions queue index '.(i%${i}).' / end' | endfor | :wq" rules-256-${i}queue
done

