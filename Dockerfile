FROM python:3-alpine

ADD crontab.txt /crontab.txt
ADD cron_script.sh /cron_script.sh
COPY entry.sh /entry.sh
COPY check_vimeo_changes.py /check_vimeo_changes.py
COPY requirements.txt /requirements.txt
RUN chmod 755 /cron_script.sh /entry.sh /check_vimeo_changes.py
RUN /usr/bin/crontab /crontab.txt
RUN apk update
RUN apk add nano
RUN pip install -r requirements.txt
RUN ln -sf /proc/1/fd/1 /var/log/script.log
CMD ["/entry.sh"]