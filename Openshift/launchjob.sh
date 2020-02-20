#!/bin/bash

responsekey=$(curl -k -X POST -d @json/jobjmeterkey.json -H "Authorization: Bearer R6vxuQvub9cjZUgjVOBh359hrOaWEyaamigXiULz_cI" -H 'Accept: application/json' -H 'Content-Type: application/json' https://cloud.leanovia.net:8443/apis/batch/v1/namespaces/jmeter/jobs)
sleep 10
responseserv=$(curl -k -X POST -d @json/jobjmeterserv.json -H "Authorization: Bearer R6vxuQvub9cjZUgjVOBh359hrOaWEyaamigXiULz_cI" -H 'Accept: application/json' -H 'Content-Type: application/json' https://cloud.leanovia.net:8443/apis/batch/v1/namespaces/jmeter/jobs)
sleep 20
responsecont=$(curl -k -X POST -d @json/jobjmetercont.json -H "Authorization: Bearer R6vxuQvub9cjZUgjVOBh359hrOaWEyaamigXiULz_cI" -H 'Accept: application/json' -H 'Content-Type: application/json' https://cloud.leanovia.net:8443/apis/batch/v1/namespaces/jmeter/jobs)


#curl -k -X POST -d @jobAPI.json -H "Authorization: Bearer $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$ENDPOINT/apis/batch/v1/namespaces/jmeter/jobs
#curl -k -X POST -d @jobAPI.json -H "Authorization: Bearer R6vxuQvub9cjZUgjVOBh359hrOaWEyaamigXiULz_cI" -H 'Accept: application/json' -H 'Cntent-Type: application/json' https://cloud.leanovia.net:8443/apis/batch/v1/namespaces/jmeter/jobs
