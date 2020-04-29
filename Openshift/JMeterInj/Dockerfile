FROM centos:7

RUN yum install java-1.8.0-openjdk-devel -y
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum update -y
RUN yum install -y python36u python36u-libs

RUN yum install wget -y
RUN wget https://www-us.apache.org/dist//jmeter/binaries/apache-jmeter-5.2.1.tgz
RUN tar -xvzf apache-jmeter-5.2.1.tgz
RUN rm -f apache-jmeter-5.2.1.tgz

COPY scriptJMeterInjBuild.sh scriptJMeterInjBuild.sh
RUN chgrp 0 scriptJMeterInjBuild.sh && \
    chmod g=u scriptJMeterInjBuild.sh && \
    chmod +x scriptJMeterInjBuild.sh

COPY scriptReturnReadiness.sh /scriptReturnReadiness.sh
RUN chgrp 0 scriptReturnReadiness.sh && \
    chmod g=u scriptReturnReadiness.sh && \
    chmod +x scriptReturnReadiness.sh

COPY jmeterRemoveIPFromCSVName.py /jmeterRemoveIPFromCSVName.py
RUN chgrp 0 jmeterRemoveIPFromCSVName.py && \
    chmod g=u jmeterRemoveIPFromCSVName.py && \
    chmod +x jmeterRemoveIPFromCSVName.py

RUN mkdir /myFiles
RUN chgrp 0 /myFiles && \
    chmod g=u /myFiles


RUN chgrp -R 0 /apache-jmeter-5.2.1 && \
    chmod -R g=u /apache-jmeter-5.2.1

USER 1001

ENTRYPOINT ["scriptJMeterInjBuild.sh"]
