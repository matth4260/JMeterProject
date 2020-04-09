#!/bin/sh
#export READY=1

cp /SharedVolume/rmi_keystore.jks /apache-jmeter-5.2.1/bin/rmi_keystore.jks
cd /apache-jmeter-5.2.1/bin/

#export READY=0
touch /myFiles/READY

echo "Verification readyness of the csv files..."
while ! test -f /SharedVolume/csvModif/READY; do
  sleep 10
done
echo "csv files ready"

export MYIP=$(hostname -I)
echo $MYIP"test"
export MYIP=`echo $MYIP | sed 's/ *$//g'`
echo $MYIP"test"
cp /SharedVolume/csvModif/*-$MYIP.csv /apache-jmeter-5.2.1/bin/
python3 /jmeterRemoveIPFromCSVName.py $MYIP


/apache-jmeter-5.2.1/bin/jmeter-server
