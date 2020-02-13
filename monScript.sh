#!/bin/sh

echo "Generating the rmi keystore"
docker run --name jmeterkey -v /Users/leanovia/Documents/Docker/SharedVolume:/SharedVolume jmeterkey
docker rm jmeterkey
echo "rmi keystore generated"

echo "Launching the servers"
for i in $(seq 1 7);
do
	echo "Launching server $i"
	docker run --name jmeterserv$i -d -v /Users/leanovia/Documents/Docker/SharedVolume:/SharedVolume jmeterserv
	echo "Server $i launched"
done

echo "Launching controler"
docker run --name jmetercont -it -v /Users/leanovia/Documents/Docker/SharedVolume:/SharedVolume jmetercont
echo "Controler launched"

echo "Stopping all containers"
for i in $(seq 1 7);
do
	echo "Removing server $i"
	docker stop jmeterserv$i
	docker rm jmeterserv$i
	echo "Server $i removed"
done
echo "Removing controler"
docker rm jmetercont
echo "Controler removed"
