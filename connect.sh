#!/bin/bash
x=$(nmap -n -sP 10.42.0.255/24)
substring='10.42.0'
stationary='10.42.0.1'
for str in $x
do
	if [ $(echo "$str" | grep -i  "$substring") ]
	then
		if [ "$str" != "$stationary" ]
		then
		ssh pi@"$str"
		exit 0
		fi
	fi
done

