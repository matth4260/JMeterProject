FROM centos:7

RUN yum install java-1.8.0-openjdk-devel -y
RUN yum install wget -y
RUN wget https://www-us.apache.org/dist//jmeter/binaries/apache-jmeter-5.2.1.tgz
RUN tar -xvzf apache-jmeter-5.2.1.tgz
RUN rm -f apache-jmeter-5.2.1.tgz

ENTRYPOINT ["apache-jmeter-5.2.1/bin/jmeter","-n","-t","/SharedVolume/JMeterTest.jmx","-l","/SharedVolume/results.jtl","-e","-o","SharedVolume/Results"]
