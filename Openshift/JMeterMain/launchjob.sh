#!/bin/bash

ENDPOINT=cloud.leanovia.net:8443
NAMESPACE=jmeter
MAXLOOP=50

echo "Launching key job"
responsekey=$(curl -k -X POST -d @json/jobjmeterkey.json -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs)
sleep 10

echo "Launching servers job"
responseserv=$(curl -k -X POST -d @json/jobjmeterserv.json -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs)

ready=False
i=1
while [ "$ready" == "False" ] && [ $i -lt  $MAXLOOP ]
do
  echo "Cheking if servers are ready"
  ready=$(curl -k     -H "Authorization: Bearer $TOKEN"     -H 'Accept: application/json'     https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmeterserv | python3 jmeterServReady.py)
  sleep 5
  i=$(($i+1))
done

if [ "$ready" == "True" ]; then
  echo "Servers ready launching controler job"
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
	echo "servers didn't start properly"
fi


