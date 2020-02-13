#!/bin/sh

echo "checking if result directory exist"
if [ -d "SharedVolume/Results" ] 
then
	echo "The directory "SharedVolume/Results" exists. You need to remove this directory to perfom the test"
	exit 0
fi

if [ -f "SharedVolume/results.jtl" ]
then
	echo "The file "SharedVolume/results.jtl" exists. You need to remove this file to perform the test"
	exit 0
fi

if [ "$1" -lt 1 ]
then
	echo "number of injectors must be greater than 0"
	exit 0
fi







echo "Launching JMeterKey container"
docker run --name jmeterkey -v /Users/leanovia/Documents/Docker/SharedVolume:/SharedVolume jmeterkey
docker rm jmeterkey
echo "Removing JMeterKey container"


echo "Launching JMeterServers containers"
for i in $(seq 1 2);
do
	echo "Launching server $i"
	docker run --name jmeterserv$i -d -v /Users/leanovia/Documents/Docker/SharedVolume:/SharedVolume jmeterserv
	echo "Server $i launched"
done
echo "All JMeterServers containers have been launched"


echo "Launching JMeterControler container"
docker run --name jmetercont -it -v /Users/leanovia/Documents/Docker/SharedVolume:/SharedVolume jmetercont
echo "JMeterControler container launched and test executed"


echo "Stopping and removing JMeterServers containers"
for i in $(seq 1 2);
do
	echo "Removing server $i"
	docker stop jmeterserv$i
	docker rm jmeterserv$i
	echo "Server $i removed"
done
echo "All JMeterServers containers have been removed"


echo "Removing JMeterControler container"
docker rm jmetercont
echo "JMeterControler container removed"

echo "Removing rmi keystore"
rm SharedVolume/rmi_keystore.jks
