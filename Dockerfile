FROM python:2.7-alpine

RUN adduser -D maxwell

WORKDIR /opt/bin/maxwell

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY backend backend
COPY migrations migrations
COPY server.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP server.py

RUN chown -R maxwell:maxwell ./
USER maxwell

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]