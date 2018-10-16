#!/bin/bash
iface=${1}
var=`ifconfig ${iface} &> /dev/null;echo "$?"`
if [ $var = 0 ]
then
    rx=`ifconfig ${iface} | tr -s ' ' | tail -n2 | head -n1 | cut -d' ' -f3|cut -d':' -f2`
    tx=`ifconfig ${iface} | tr -s ' ' | tail -n2 | head -n1 | cut -d' ' -f7| cut -d':' -f2`
    echo "${rx}:${tx}"
else
    echo "interface does not exist."
fi