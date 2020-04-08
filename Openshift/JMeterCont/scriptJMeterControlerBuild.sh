#!/bin/sh

list_ips=$(echo $(dig jmeter-serv.jmeter 1 +search +short) | sed 's/ /,/g')
echo "Liste des ips : $list_ips"
cp /SharedVolume/rmi_keystore.jks /apache-jmeter-5.2.1/bin/rmi_keystore.jks
cd /apache-jmeter-5.2.1/bin/
cp /SharedVolume/JMeterTest.jmx /apache-jmeter-5.2.1/bin/JMeterTest.jmx

/apache-jmeter-5.2.1/bin/jmeter -n -R$list_ips -X -t ./JMeterTest.jmx -l /SharedVolume/results.jtl -e -o /SharedVolume/Results
