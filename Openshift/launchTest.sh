#!/bin/sh


#$1 = number of injectors
[ -z "$1" ] && echo "You must choose the number of injectors (parameter one)" && exit 0

[ "$1" -lt 1 ] && echo "number of injectors must be greater than 0" && exit 0

#$2 = shared volume path
[ -z "$2" ] && echo "you must specify the folder where your test is and where your results will go (parameter two)" && exit 0

[ -d "$2/Results" ] && echo "The directory "SharedVolume/Results" exists. You need to remove this directory to perfom the test" && exit 0

[ -f "$2/results.jtl" ] && echo "The file "SharedVolume/results.jtl" exists. You need to remove this file to perform the test" && exit 0 

#docker network create --attachable JMeter_Network


echo "Launching JMeterKey container"
docker run --name jmeterkey -v "$2":/SharedVolume jmeterkey
docker rm jmeterkey
echo "Removing JMeterKey container"


echo "Launching JMeterServers containers"
for i in $(seq 1 $1);
do
	echo "Launching server $i"
	docker run --name jmeterserv$i --network=JMeter_Network -d -v "$2":/SharedVolume jmeterserv
	#docker network connect JMeter_Network jmeterserv$i
	echo "Server $i launched"
done
echo "All JMeterServers containers have been launched"


echo "Launching JMeterControler container"
docker run --name jmetercont --network=JMeter_Network -it -v "$2":/SharedVolume -e NUMBER_OF_INJECTORS=$1 jmetercont
#docker network connect JMeter_Network jmetercont
echo "JMeterControler container launched and test executed"


echo "Stopping and removing JMeterServers containers"
for i in $(seq 1 $1);
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
rm $2/rmi_keystore.jks

#docker network rm JMeter_Network
