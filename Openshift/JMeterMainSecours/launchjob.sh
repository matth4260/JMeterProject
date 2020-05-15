#!/bin/bash

ENDPOINT=cloud.leanovia.net:8443
NAMESPACE=jmeter
MAXLOOP=${WAITING_TIME_MULTIPLIER}
MAXWAITINGTIME=${TEST_MAX_DURATION}


timeNow=$(date +%Y%m%d%H%M)

openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/oc login -u $USER -p $PASSWORD -n jmeter -s https://cloud.leanovia.net:8443 --insecure-skip-tls-verify
TOKEN=$(openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/oc whoami -t)
echo "Changing numbers in all scripts to respect job number"
nbJob=$(python3 jmeterChangeSecoursNumber.py)
mv /SharedVolume/injectorToRelaunch.txt /SharedVolume/injectorToRelaunch${nbJob}.txt
rm /SharedVolume/csvModif/READY





FILE=/SharedVolume/rmi_keystore.jks
if test -f "$FILE"; then
  echo "creating headless service"
  reponseHeadlessService=$(curl -k -X POST -d @json/injHeadlessService.json -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/services)


  echo "Launching Injectors job"
  responseInj=$(curl -k -X POST -d @json/jobjmeterinj.json -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs)

  ready=False
  i=0
  while [ "$ready" == False ] && [ $i -lt  $MAXLOOP ]
  do
    echo "Checking if Injectors are ready"
    ready=$(curl -k     -H "Authorization: Bearer $TOKEN"     -H 'Accept: application/json'     https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmeterinj${nbJob} | python3 jmeterInjReady.py)
    sleep 10
    i=$(($i+1))
  done

  if [ "$ready" == "True" ]; then
    echo "The Injectors are ready"

    #Récupérer la liste des ips
    echo "liste des ips : "
    export LIST_IP=$(echo $(dig jmeter-Inj${nbJob}.jmeter 1 +search +short) | sed 's/ /,/g')
    echo $LIST_IP

    echo "managing csv"
    python3 manageCSV.py ${nbJob} $LIST_IP
    touch /SharedVolume/csvModif/READY
    response="True"

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
          finished=$(curl -k     -H "Authorization: Bearer $TOKEN"     -H 'Accept: application/json'     https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmeterinj${nbJob} | python3 jmeterInjEnded.py )
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
        responsedeletecont=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs/jobjmetercontsecours${nbJob})
        responsedeletecont=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmetercontsecours${nbJob})
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
  responsedeleteInj=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs/jobjmeterinj${nbJob})
  responsedeleteInj=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmeterinj${nbJob})

  echo "removing headless service"
  responseheadless=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/services/jmeter-inj${nbJob})
  
else
  echo "rmi_keystore couldn't be found"
  echo "Stopping the test"
fi

echo "Starting ending session"




FILE=/SharedVolume/results${nbJob}.jtl
if test -f "$FILE"; then

  echo "moving results${nbJob}.jtl"
  mv /SharedVolume/results${nbJob}.jtl /SharedVolume/results/$timeNow-results${nbJob}.jtl
  echo "results${nbJob}.jtl moved"

fi

FILE=/SharedVolume/Results${nbJob}
if [ -d "$FILE" ]; then

  echo "moving Results folder"
  mv /SharedVolume/Results${nbJob} /SharedVolume/results/$timeNow-Results${nbJob}
  echo "Results folder moved"

fi

FILE=/SharedVolume/injectorToRelaunch${nbJob}.txt
if [ -f "$FILE" ]; then

  echo "removing injectorToRelaunch${nbJob}.txt"
  rm /SharedVolume/injectorToRelaunch${nbJob}.txt
  echo "Removed injectorToRelaunch${nbJob}.txt"

fi




echo "Ending session finished"






responsedeletemain=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/$NAMESPACE/jobs/jobjmetermainsecours${nbJob})
responsedeletemain=$(curl -k -X DELETE -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' https://$ENDPOINT/api/v1/namespaces/$NAMESPACE/pods?labelSelector=job-name=jobjmetermainsecours${nbJob})
