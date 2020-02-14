#!/bin/sh

docker run -p 3000:3000 --name grafana -d  grafana/grafana
docker run -d -p 8086:8086 -p 2003:2003 -p 8088:8088 --name influxdb --network=JMeter_Network myinfluxdb
docker exec influxdb influx -execute "CREATE DATABASE jmeter"
