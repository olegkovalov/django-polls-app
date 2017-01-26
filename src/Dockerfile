FROM python:3.5.2-alpine

ENV POLLS_GUNICORN_NUMBER_OF_WORKERS=2

RUN apk update && apk add \
    build-base \
    jpeg-dev \
    zlib-dev \
    libpq \
    postgresql-dev \
    gettext

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY docker-entrypoint-api.sh /docker-entrypoint-api.sh
RUN chmod +x /docker-entrypoint-api.sh

COPY docker-entrypoint-celery.sh /docker-entrypoint-celery.sh
RUN chmod +x /docker-entrypoint-celery.sh

COPY . /polls

WORKDIR /polls

VOLUME /polls
VOLUME /polls/public

EXPOSE 8000

ENTRYPOINT /docker-entrypoint-api.sh
