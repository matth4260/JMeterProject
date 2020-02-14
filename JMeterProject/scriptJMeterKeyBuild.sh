#!/bin/sh

echo "creating rmi keystore"
keytool -genkey -keyalg RSA -alias rmi -keystore rmi_keystore.jks -storepass changeit -keypass changeit -validity 7 -keysize 2048 -dname "CN=a OU=a O=a L=a ST=a C=a"
echo "rmi keystore created"
echo "moving rmi keystore to shared location"
mv /rmi_keystore.jks /SharedVolume/rmi_keystore.jks

