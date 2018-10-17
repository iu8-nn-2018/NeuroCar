#!/bin/bash
ip=$(./connect.sh)
for param in "$@"
do

	if [ -f "$param" ];
	then
	scp "$param" pi@"$ip":/home/pi/Project/"$param"
	elif [ -d "$param" ];
	then
	tar -cvf "$param".tar.gz "$param"
	scp "$param".tar.gz pi@"$ip":/home/pi/Project/"$param".tar.gz
	rm "$param".tar.gz
	sshpass ssh pi@"$ip"  tar -xvf /home/pi/Project/"$param".tar.gz -C /home/pi/Project/
	sshpass ssh pi@"$ip" rm /home/pi/Project/"$param".tar.gz
	fi
done
