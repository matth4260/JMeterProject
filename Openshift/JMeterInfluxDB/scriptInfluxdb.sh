#!/bin/sh

if ! whoami &> /dev/null; then
  if [ -w /etc/passwd ]; then
    echo "${USER_NAME:-default}:x:$(id -u):0:${USER_NAME:-default} user:${HOME}:/sbin/nologin" >> /etc/passwd
  fi
fi

set -e

if [ "${1:0:1}" = '-' ]; then
    set -- influxd "$@"
fi

if [ "$1" = 'influxd' ]; then
        /init-influxdb.sh "${@:2}"
fi

exec "$@"


#/init-influxdb.sh
#/bin/bash
#influxd -config /influxdb.conf
#influx -execute "CREATE DATABASE jmeter"
