#!/bin/bash

ENDPOINT=cloud.leanovia.net:8443
NAMESPACE=jmeter
MAXLOOP=${WAITING_TIME_MULTIPLIER}
MAXWAITINGTIME=${TEST_MAX_DURATION}


timeNow=$(date +%Y%m%d%H%M)

openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/oc login -u $USER -p $PASSWORD -n jmeter -s https://cloud.leanovia.net:8443 --insecure-skip-tls-verify
TOKEN=$(openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/oc whoami -t)
echo "Launching key job"
responsekey=$(curl -k -X POST -d @json/jobjmeterkey.json -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs)

echo "Integrating jmx with Dynatrace"
python3 integrateur_jmeter-dynatrace.py /SharedVolume/${JMX_NAME}.jmx /SharedVolume/${JSON_NAME}.json -t /SharedVolume/dynatrace-${JMX_NAME}.jmx
echo "launching used csv script"
python3 jmeterRemoveUsedLinesInCSV.py
echo "used csv script done"


ready=False
i=0
while [ "$ready" == False ] && [ $i -lt  $MAXLOOP ]
do
  echo "Checking if key container is done"
  ready=$(curl -k     -H "Authorization: Bearer $TOKEN"     -H 'Accept: application/json'     https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmeterkey | python3 jmeterInjEnded.py)
  sleep 10
	i=$(($i+1))
done

FILE=/SharedVolume/rmi_keystore.jks
if test -f "$FILE"; then
  echo "rmi_keystore generated"
  response=$(python3 jmeterInjChangeNumberInjector.py)
  echo "Launching Injectors job"
  responseInj=$(curl -k -X POST -d @json/jobjmeterinj.json -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs)

  ready=False
  i=0
  while [ "$ready" == False ] && [ $i -lt  $MAXLOOP ]
  do
    echo "Checking if Injectors are ready"
    ready=$(curl -k     -H "Authorization: Bearer $TOKEN"     -H 'Accept: application/json'     https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmeterinj | python3 jmeterInjReady.py)
    sleep 10
    i=$(($i+1))
  done

  if [ "$ready" == "True" ]; then
    echo "The Injectors are ready"

    #Récupérer la liste des ips
    echo "liste des ips : "
    export LIST_IP=$(echo $(dig jmeter-Inj.jmeter 1 +search +short) | sed 's/ /,/g')
    echo $LIST_IP

    echo "Découpage des fichiers CSVs"
    response=$(python3 jmeterDecoupeCSV.py $LIST_IP)
    echo "Fin découpage"

    if [ "$response" == "True" ]; then
      echo "Découpage bien effectué"
      ready=False
      i=1
      while [ "$ready" == "False" ] && [ $i -lt  $MAXLOOP ]
      do
        echo "Cheking if Injectors are waiting for controler"
        
        ipsAvecEspace=${LIST_IP//,/ }

        ready=True

        for ip in $ipsAvecEspace
        do
          curl $ip":1099"
          reponse=$?
          if [ $reponse != 0 ];
          then
            ready=False
          fi
        done

        sleep 10
        i=$(($i+1))
      done

      if [ "$ready" == "True" ]; then
        echo "JMeter Injectors started properly, launching controler job"
        responsecont=$(curl -k -X POST -d @json/jobjmetercont.json -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs)
        finished="False"
        i=0
        FILE=/SharedVolume/stopTest
        while [ $finished == "False" ] && [ $i -lt  $MAXWAITINGTIME ] && ! test -f "$FILE";
        do
          echo "checking if Injectors are finished"
          sleep 60
          finished=$(curl -k     -H "Authorization: Bearer $TOKEN"     -H 'Accept: application/json'     https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmetercont | python3 jmeterInjEnded.py )
          i=$(($i+1))
        done
        if [ "$finished" == "True" ]; then
          echo "Test finished"
          echo "Waiting for results' transfer"
          
          FILE=/Results/resultsTransfered
          READY="False"
          while [ $READY == "False" ] && [ $i -lt $MAXLOOP ]
          do
            sleep 10
            echo "cheking if file exist"
            if test -f "$FILE"; then
              echo "file exist"
              READY="True"
            fi
          done

        else
          if [ $i -lt $MAXWAITINGTIME ]; then
            echo "Test took too long to finish, now stopping it"
          else
            echo "Order to stop the test was given"
          fi
        fi
        echo "closing controler job and container"
        responsedeletecont=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs/jobjmetercont)
        responsedeletecont=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmetercont)
      else
        echo "jmeter Injectors didn't start properly"
      fi
    
    else
      echo "Problème avec le découpage des csv"
    fi


  else
    echo "The Injectors didn't start properly"
  fi
  echo "Stopping the Injer job, and the Injectors' containers"
  responsedeleteInj=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs/jobjmeterinj)
  responsedeleteInj=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmeterinj)

  
else
  echo "rmi_keystore couldn't be generated"
  echo "Stopping the test"
fi

echo "Starting ending session"



FILE=/SharedVolume/rmi_keystore.jks
if test -f "$FILE"; then
  echo "deleting rmi keystore"
  rm /SharedVolume/rmi_keystore.jks
  echo "rmi keystore deleted"
fi

FILE=/SharedVolume/results.jtl
if test -f "$FILE"; then

  echo "moving results.jtl"
  mv /SharedVolume/results.jtl /SharedVolume/results/$timeNow-results.jtl
  echo "results.jtl moved"

fi

FILE=/SharedVolume/Results
if [ -d "$FILE" ]; then

  echo "moving Results folder"
  mv /SharedVolume/Results /SharedVolume/results/$timeNow-Results
  echo "Results folder moved"

fi

FILE=/SharedVolume/stopTest
if test -f "$FILE"; then

  echo "deleting stopTest"
  rm /SharedVolume/stopTest
  echo "stopTest deleted"

fi

FILE=/SharedVolume/csvModif/READY
if test -f "$FILE"; then

  echo "deleting READY file in csvModif"
  rm /SharedVolume/csvModif/READY
  echo "READY file in csvModif deleted"

fi

echo "Ending session finished"



echo "Stopping key job and container"
responsedeletekey=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs/jobjmeterkey)
responsedeletekey=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmeterkey)
echo "all jobs and pods closed"




responsedeletemain=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs/jobjmetermain)
responsedeletemain=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmetermain)
