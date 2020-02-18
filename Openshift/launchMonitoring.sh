#!/bin/sh

docker run -p 3000:3000 --name grafana -d  grafana/grafana
docker run -it -p 8086:8086 -p 2003:2003 -p 8088:8088 --name influxdb --network=JMeter_Network -e INFLUXDB_DB=jmeter myinfluxdb