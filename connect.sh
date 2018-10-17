#!/bin/bash
x=$(cat /var/lib/misc/dnsmasq.leases)
y=$( echo "$x" | grep -i  "raspberry" )
for i in $(echo $y | tr " " "\n")
do
	if [[ "$i" =~ "10.42.0" ]]
	then
 	echo "$i"
	fi
done
