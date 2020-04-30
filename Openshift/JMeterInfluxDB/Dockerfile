FROM centos:7

COPY influxdb.repo /etc/yum.repos.d/influxdb.repo
RUN yum install influxdb -y

COPY influxdb.conf /influxdb.conf 

COPY init-influxdb.sh /init-influxdb.sh
RUN chgrp 0 /init-influxdb.sh && \
    chmod g=u /init-influxdb.sh && \
    chmod +x /init-influxdb.sh

COPY entrypoint.sh /entrypoint.sh
RUN chgrp 0 /entrypoint.sh && \
    chmod g=u /entrypoint.sh && \
    chmod +x /entrypoint.sh

RUN mkdir /var/lib/influxdb/meta && \
    chgrp -R 0 /var/lib/influxdb && \
    chmod -R g=u /var/lib/influxdb

RUN touch /.influx_history && \
    chgrp 0 /.influx_history && \
    chmod g=u /.influx_history

RUN chmod g=u /etc/passwd
USER 1001

EXPOSE 8086
EXPOSE 8088
EXPOSE 2003

ENTRYPOINT ["/entrypoint.sh"]
CMD ["influxd"]
