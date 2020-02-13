#!/bin/sh

cp /SharedVolume/rmi_keystore.jks /rmi_keystore.jks
/apache-jmeter-5.2.1/bin/jmeter -n -R172.17.0.2,172.17.0.3 -t /SharedVolume/JMeterTest.jmx -l /SharedVolume/results.jtl -e -o /SharedVolume/Results
