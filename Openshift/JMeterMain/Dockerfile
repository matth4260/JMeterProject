FROM centos:7

RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum update -y
RUN yum install -y python36u python36u-libs
RUN yum install wget -y
RUN wget https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz
RUN tar xzvf openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz 
RUN yum install bind-utils -y

COPY launchjob.sh /launchjob.sh
RUN chgrp 0 launchjob.sh && \
    chmod g=u launchjob.sh && \
    chmod +x launchjob.sh


COPY jmeterServUp.py /jmeterServUp.py
RUN chgrp 0 jmeterServUp.py && \
    chmod g=u jmeterServUp.py && \
    chmod +x jmeterServUp.py

COPY jmeterServReady.py /jmeterServReady.py
RUN chgrp 0 jmeterServReady.py && \
    chmod g=u jmeterServReady.py && \
    chmod +x jmeterServReady.py

COPY jmeterServEnded.py /jmeterServEnded.py
RUN chgrp 0 jmeterServEnded.py && \
    chmod g=u jmeterServEnded.py && \
    chmod +x jmeterServEnded.py

COPY jmeterServChangeNumberInjector.py /jmeterServChangeNumberInjector.py
RUN chgrp 0 jmeterServChangeNumberInjector.py && \
    chmod g=u jmeterServChangeNumberInjector.py && \
    chmod +x jmeterServChangeNumberInjector.py

RUN mkdir json
RUN mkdir /.kube && \
    chgrp 0 /.kube && \
    chmod g=u /.kube

COPY json/jobjmetercont.json /json/jobjmetercont.json
RUN chgrp 0 json/jobjmetercont.json && \
    chmod g=u json/jobjmetercont.json

COPY json/jobjmeterkey.json /json/jobjmeterkey.json
RUN chgrp 0 json/jobjmeterkey.json && \
    chmod g=u json/jobjmeterkey.json

COPY json/jobjmeterserv.json /json/jobjmeterserv.json
RUN chgrp 0 json/jobjmeterserv.json && \
    chmod g=u json/jobjmeterserv.json

COPY jmeterDecoupeCSV.py /jmeterDecoupeCSV.py
RUN chgrp 0 jmeterDecoupeCSV.py && \
    chmod g=u jmeterDecoupeCSV.py && \
    chmod +x jmeterDecoupeCSV.py

USER 1001

ENTRYPOINT ["/launchjob.sh"]
#ENTRYPOINT ["/bin/bash"]

