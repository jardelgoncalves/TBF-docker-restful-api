#!/bin/bash
user=${1}
pass=${2}

veth=${3}
rate=${4}
burst=${5}
lat=${6}
peak=${7}
minburst=${8}

var=`ifconfig ${veth} &> /dev/null;echo "$?"`
if [ $var = 0 ]
then
    echo $pass | sudo -S -u ${user} sh -c "tc qdisc add dev ${veth} root tbf rate ${rate} latency ${lat} burst ${burst} peakrate ${peak} minburst ${minburst} 2> /dev/null"
    if [ $? = 0 ]
    then
        echo "0"
    else
        echo "2"
    fi
else
    echo "1"
fi