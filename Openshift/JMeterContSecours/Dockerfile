FROM centos:7

RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum update -y
RUN yum install -y python36u python36u-libs
RUN yum install java-1.8.0-openjdk-devel -y
RUN yum install wget -y
RUN yum install bind-utils -y
RUN wget https://www-us.apache.org/dist//jmeter/binaries/apache-jmeter-5.2.1.tgz


RUN tar -xvzf apache-jmeter-5.2.1.tgz
RUN chgrp -R 0 /apache-jmeter-5.2.1 && \
    chmod -R g=u /apache-jmeter-5.2.1
RUN rm -f apache-jmeter-5.2.1.tgz

COPY scriptJMeterControlerBuild.sh /scriptJMeterControlerBuild.sh
RUN chgrp -R 0 scriptJMeterControlerBuild.sh && \
    chmod -R g=u scriptJMeterControlerBuild.sh && \
    chmod +x scriptJMeterControlerBuild.sh

RUN mkdir FolderForRMI
RUN chgrp -R 0 FolderForRMI && \
    chmod -R g=u FolderForRMI

COPY findJobNumber.py /findJobNumber.py
RUN chgrp 0 findJobNumber.py && \
    chmod g=u findJobNumber.py && \
    chmod +x findJobNumber.py


ENTRYPOINT ["/scriptJMeterControlerBuild.sh"]
USER 1001
