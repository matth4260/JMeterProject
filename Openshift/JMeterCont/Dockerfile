FROM centos:7

RUN yum install java-1.8.0-openjdk-devel -y
RUN yum install wget -y
RUN wget https://www-us.apache.org/dist//jmeter/binaries/apache-jmeter-5.2.1.tgz
RUN wget https://github.com/NovatecConsulting/JMeter-InfluxDB-Writer/releases/download/v-1.2/JMeter-InfluxDB-Writer-plugin-1.2.jar

RUN chgrp -R 0 JMeter-InfluxDB-Writer-plugin-1.2.jar && \
    chmod -R g=u JMeter-InfluxDB-Writer-plugin-1.2.jar
RUN tar -xvzf apache-jmeter-5.2.1.tgz
RUN chgrp -R 0 /apache-jmeter-5.2.1 && \
    chmod -R g=u /apache-jmeter-5.2.1
RUN rm -f apache-jmeter-5.2.1.tgz
RUN mv JMeter-InfluxDB-Writer-plugin-1.2.jar /apache-jmeter-5.2.1/lib/ext/

COPY scriptJMeterControlerBuild.sh /scriptJMeterControlerBuild.sh
RUN chgrp -R 0 scriptJMeterControlerBuild.sh && \
    chmod -R g=u scriptJMeterControlerBuild.sh

ENTRYPOINT ["/scriptJMeterControlerBuild.sh"]
USER 1001
