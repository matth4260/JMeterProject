#!/bin/sh

list_ips=jmeterserv1
if [ $NUMBER_OF_INJECTORS -gt 1 ]
then
	for i in $(seq 2 $NUMBER_OF_INJECTORS);
	do
		ip=",jmeterserv$i"
		list_ips=$list_ips$ip
	done
fi
echo "$list_ips"
cp /SharedVolume/rmi_keystore.jks /rmi_keystore.jks
/apache-jmeter-5.2.1/bin/jmeter -n -R$list_ips -t /SharedVolume/JMeterTest.jmx -l /SharedVolume/results.jtl -e -o /SharedVolume/Results
