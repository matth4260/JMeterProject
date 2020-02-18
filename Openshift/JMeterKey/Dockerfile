FROM centos:7

RUN yum install java-1.8.0-openjdk-devel -y

RUN yum install wget -y
RUN wget https://www-us.apache.org/dist//jmeter/binaries/apache-jmeter-5.2.1.tgz
RUN tar -xvzf apache-jmeter-5.2.1.tgz
RUN rm -f apache-jmeter-5.2.1.tgz

COPY scriptJMeterKey.sh /scriptJMeterKey.sh
RUN chgrp 0 /scriptJMeterKey.sh && \
    chmod g=u /scriptJMeterKey.sh && \
    chmod +x /scriptJMeterKey.sh

ENTRYPOINT ["/scriptJMeterKeyBuild.sh"]
