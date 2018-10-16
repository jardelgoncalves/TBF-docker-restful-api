#!/bin/bash
var=`ifconfig ${1} &> /dev/null;echo "$?"`
user=${2}
pass=${3} 
if [ $var = 0 ]
then
    echo $pass | sudo -S -u ${user} sh -c "tc qdisc del root dev ${1}"
    echo "0"
else
    echo "1"
fi 