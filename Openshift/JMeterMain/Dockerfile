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


COPY jmeterInjUp.py /jmeterInjUp.py
RUN chgrp 0 jmeterInjUp.py && \
    chmod g=u jmeterInjUp.py && \
    chmod +x jmeterInjUp.py

COPY jmeterInjReady.py /jmeterInjReady.py
RUN chgrp 0 jmeterInjReady.py && \
    chmod g=u jmeterInjReady.py && \
    chmod +x jmeterInjReady.py

COPY jmeterInjEnded.py /jmeterInjEnded.py
RUN chgrp 0 jmeterInjEnded.py && \
    chmod g=u jmeterInjEnded.py && \
    chmod +x jmeterInjEnded.py

COPY jmeterInjChangeNumberInjector.py /jmeterInjChangeNumberInjector.py
RUN chgrp 0 jmeterInjChangeNumberInjector.py && \
    chmod g=u jmeterInjChangeNumberInjector.py && \
    chmod +x jmeterInjChangeNumberInjector.py

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

COPY json/jobjmeterinj.json /json/jobjmeterinj.json
RUN chgrp 0 json/jobjmeterinj.json && \
    chmod g=u json/jobjmeterinj.json

COPY json/injHeadlessService.json /json/injHeadlessService.json
RUN chgrp 0 json/injHeadlessService.json && \
    chmod g=u json/injHeadlessService.json

COPY json/jobjmetermainsecours.json /json/jobjmetermainsecours.json
RUN chgrp 0 json/jobjmetermainsecours.json && \
    chmod g=u json/jobjmetermainsecours.json

COPY jmeterDecoupeCSV.py /jmeterDecoupeCSV.py
RUN chgrp 0 jmeterDecoupeCSV.py && \
    chmod g=u jmeterDecoupeCSV.py && \
    chmod +x jmeterDecoupeCSV.py

COPY jmeterRemoveUsedLinesInCSV.py /jmeterRemoveUsedLinesInCSV.py
RUN chgrp 0 jmeterRemoveUsedLinesInCSV.py && \
    chmod g=u jmeterRemoveUsedLinesInCSV.py && \
    chmod +x jmeterRemoveUsedLinesInCSV.py

RUN mkdir /Results && \
    chgrp 0 /Results && \
    chmod g=u /Results

COPY integrateur_jmeter-dynatrace.py /integrateur_jmeter-dynatrace.py
RUN chgrp 0 integrateur_jmeter-dynatrace.py && \
    chmod g=u integrateur_jmeter-dynatrace.py && \
    chmod +x integrateur_jmeter-dynatrace.py

COPY jmeterManageCrashedInj.py /jmeterManageCrashedInj.py
RUN chgrp 0 jmeterManageCrashedInj.py && \
    chmod g=u jmeterManageCrashedInj.py && \
    chmod +x jmeterManageCrashedInj.py

COPY jmeterChangeSecoursNumber.py /jmeterChangeSecoursNumber.py
RUN chgrp 0 jmeterChangeSecoursNumber.py && \
    chmod g=u jmeterChangeSecoursNumber.py && \
    chmod +x jmeterChangeSecoursNumber.py




USER 1001

ENTRYPOINT ["/launchjob.sh"]
#ENTRYPOINT ["/bin/bash"]
