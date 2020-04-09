FROM centos:7

RUN yum install java-1.8.0-openjdk-devel -y
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum update -y
RUN yum install -y python36u python36u-libs

RUN yum install wget -y
RUN wget https://www-us.apache.org/dist//jmeter/binaries/apache-jmeter-5.2.1.tgz
RUN tar -xvzf apache-jmeter-5.2.1.tgz
RUN rm -f apache-jmeter-5.2.1.tgz

COPY scriptJMeterServerBuild.sh /scriptJMeterServerBuild.sh
RUN chgrp 0 /scriptJMeterServerBuild.sh && \
    chmod g=u /scriptJMeterServerBuild.sh && \
    chmod +x /scriptJMeterServerBuild.sh

COPY scriptReturnReadiness.sh /scriptReturnReadiness.sh
RUN chgrp 0 scriptReturnReadiness.sh && \
    chmod g=u scriptReturnReadiness.sh && \
    chmod +x scriptReturnReadiness.sh

COPY jmeterRemoveIPFromCSVName.py /jmeterRemoveIPFromCSVName.py
RUN chgrp 0 jmeterRemoveIPFromCSVName.py && \
    chmod g=u jmeterRemoveIPFromCSVName.py && \
    chmod +x jmeterRemoveIPFromCSVName.py

RUN wget https://github.com/NovatecConsulting/JMeter-InfluxDB-Writer/releases/download/v-1.2/JMeter-InfluxDB-Writer-plugin-1.2.jar
RUN mv JMeter-InfluxDB-Writer-plugin-1.2.jar /apache-jmeter-5.2.1/lib/ext/
RUN chgrp 0 /apache-jmeter-5.2.1/lib/ext/JMeter-InfluxDB-Writer-plugin-1.2.jar && \
    chmod g=u /apache-jmeter-5.2.1/lib/ext/JMeter-InfluxDB-Writer-plugin-1.2.jar && \
    chmod +x /apache-jmeter-5.2.1/lib/ext/JMeter-InfluxDB-Writer-plugin-1.2.jar

RUN mkdir /myFiles
RUN chgrp 0 /myFiles && \
    chmod g=u /myFiles


RUN chgrp -R 0 /apache-jmeter-5.2.1 && \
    chmod -R g=u /apache-jmeter-5.2.1

USER 1001

ENTRYPOINT ["/scriptJMeterServerBuild.sh"]
