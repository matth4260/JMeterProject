#!/bin/sh

/bin/bash
echo "creating rmi keystore"
keytool -genkey -keyalg RSA -alias rmi -keystore /SharedVolume/rmi_keystore.jks -storepass changeit -keypass changeit -validity 7 -keysize 2048 -dname "CN=a OU=a O=a L=a ST=a C=a"
echo "rmi keystore created"
