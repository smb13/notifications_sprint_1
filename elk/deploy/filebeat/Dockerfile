FROM elastic/filebeat:8.12.0
COPY filebeat.yaml /usr/share/filebeat/filebeat.yml
USER root
RUN chown -R root /usr/share/filebeat/
RUN chmod -R go-w /usr/share/filebeat/
