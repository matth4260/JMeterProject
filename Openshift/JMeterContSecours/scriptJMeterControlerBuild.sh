#!/bin/sh


nbJob=$(python3 findJobNumber.py)
echo $nbJob
rm /SharedVolume/nbSecours${nbJob}
rm /SharedVolume/secoursLaunched
list_ips=$(echo $(dig jmeter-inj$nbJob.jmeter 1 +search +short) | sed 's/ /,/g')
echo "Liste des ips : $list_ips"
cp /SharedVolume/rmi_keystore.jks /apache-jmeter-5.2.1/bin/rmi_keystore.jks
cd /apache-jmeter-5.2.1/bin/
cp /SharedVolume/dynatrace-${JMX_NAME}.jmx /apache-jmeter-5.2.1/bin/dynatrace-${JMX_NAME}.jmx

/apache-jmeter-5.2.1/bin/jmeter -n -R $list_ips -X -t dynatrace-${JMX_NAME}.jmx -l /SharedVolume/results${nbJob}.jtl -e -o /SharedVolume/Results${nbJob}
