FROM centos:7

RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum update -y
RUN yum install -y python36u python36u-libs

COPY launchjob.sh /launchjob.sh
RUN chgrp 0 launchjob.sh && \
    chmod g=u launchjob.sh && \
    chmod +x launchjob.sh

COPY jmeterServReady.py /jmeterServReady.py
RUN chgrp 0 jmeterServReady.py && \
    chmod g=u jmeterServReady.py && \
    chmod +x jmeterServReady.py

COPY jmeterServEnded.py /jmeterServEnded.py
RUN chgrp 0 jmeterServEnded.py && \
    chmod g=u jmeterServEnded.py && \
    chmod +x jmeterServEnded.py

RUN mkdir json

COPY json/jobjmetercont.json /json/jobjmetercont.json
RUN chgrp 0 json/jobjmetercont.json && \
    chmod g=u json/jobjmetercont.json

COPY json/jobjmeterkey.json /json/jobjmeterkey.json
RUN chgrp 0 json/jobjmeterkey.json && \
    chmod g=u json/jobjmeterkey.json

COPY json/jobjmeterserv.json /json/jobjmeterserv.json
RUN chgrp 0 json/jobjmeterserv.json && \
    chmod g=u json/jobjmeterserv.json

USER 1001

ENTRYPOINT ["/launchjob.sh"]
#ENTRYPOINT ["/bin/bash"]

