#!/bin/bash

for c in $(docker ps -q); do
    iflink=`docker exec -it ${c} cat /sys/class/net/eth0/iflink`
    iflink=`echo $iflink|tr -d '\r'`
    veth=`grep -l $iflink /sys/class/net/veth*/ifindex`
    veth=`echo $veth|sed -e 's;^.*net/\(.*\)/ifindex$;\1;'`
    r=`tc qdisc show dev ${veth}`
    qos=`echo ${r} | grep "tbf"`
    ip=`docker inspect --format '{{ .NetworkSettings.IPAddress }}' ${c}`
    if [ ! -z "${qos}" ]
    then
        echo "${ip}=${veth}=${r}=${c}"
    fi
done
