#!/bin/bash

ENDPOINT=cloud.leanovia.net:8443
NAMESPACE=jmeter
MAXLOOP=50

openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/oc login -u $USER -p $PASSWORD -n jmeter -s https://cloud.leanovia.net:8443 --insecure-skip-tls-verify
TOKEN=$(openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/oc whoami -t)
echo "Launching key job"
responsekey=$(curl -k -X POST -d @json/jobjmeterkey.json -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs)

ready=False
i=0
while [ "$ready" == False ] && [ $i -lt  $MAXLOOP ]
do
  echo "Checking if key container is done"
  ready=$(curl -k     -H "Authorization: Bearer $TOKEN"     -H 'Accept: application/json'     https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmeterkey | python3 jmeterServEnded.py)
  sleep 10
	i=$(($i+1))
done

FILE=/SharedVolume/rmi_keystore.jks
if test -f "$FILE"; then
  echo "rmi_keystore generated"
  response=$(python3 jmeterServChangeNumberInjector.py)
  echo response
  echo "Launching servers job"
  responseserv=$(curl -k -X POST -d @json/jobjmeterserv.json -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs)

  ready=False
  i=0
  while [ "$ready" == False ] && [ $i -lt  $MAXLOOP ]
  do
    echo "Checking if servers are ready"
    ready=$(curl -k     -H "Authorization: Bearer $TOKEN"     -H 'Accept: application/json'     https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmeterserv | python3 jmeterServReady.py)
    sleep 10
  done

  if [ "$ready" == "True" ]; then
    echo "The servers are ready"

    #Récupérer la liste des ips
    echo "liste des ips : "
    export LIST_IP=$(echo $(dig jmeter-serv.jmeter 1 +search +short) | sed 's/ /,/g')
    echo $LIST_IP

    echo "Découpage des fichiers CSVs"
    response=$(python3 jmeterDecoupeCSV.py $LIST_IP)
    echo "Fin découpage"


    ready=False
    i=1
    while [ "$ready" == "False" ] && [ $i -lt  $MAXLOOP ]
    do
      echo "Cheking if servers are waiting for controler"
      
      ipsAvecEspace=${LIST_IP//,/ }

      ready=True

      for ip in $ipsAvecEspace
      do
        curl $ip":1099"
        reponse=$?
        if [ $reponse != 0 ];
        then
          eady=False
        fi
      done

      sleep 5
      i=$(($i+1))
    done

    if [ "$ready" == "True" ]; then
      echo "JMeter servers didn't start properly, launching controler job"
      responsecont=$(curl -k -X POST -d @json/jobjmetercont.json -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs)
      finished="False"
      while [ $finished == "False" ]
      do
        echo "checking if servers are finished"
        sleep 5
        finished=$(curl -k     -H "Authorization: Bearer $TOKEN"     -H 'Accept: application/json'     https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmetercont | python3 jmeterServEnded.py )

      done
      echo "closing jobs"
      responsedeletekey=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs/jobjmeterkey)
      responsedeleteserv=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs/jobjmeterserv)
      responsedeletecont=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs/jobjmetercont)
      responsedeletekey=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmeterkey)
      responsedeleteserv=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmeterserv)
      responsedeletecont=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmetercont)
      echo "all jobs and pods closed"
    else
      echo "jmeter servers didn't start properly"
    fi

  else
    echo "The servers didn't start properly"
  fi


  
else
  echo "rmi_keystore couldn't be generated"
  echo "Stopping the test"
fi




