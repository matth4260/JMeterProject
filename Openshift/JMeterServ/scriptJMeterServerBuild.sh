#!/bin/sh

cp /SharedVolume/rmi_keystore.jks /apache-jmeter-5.2.1/bin/rmi_keystore.jks
cd /apache-jmeter-5.2.1/bin/
/apache-jmeter-5.2.1/bin/jmeter-server
