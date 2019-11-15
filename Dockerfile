# Pull Python image within Alpine Linux
FROM python:3.7-alpine
MAINTAINER Alican Donmez - alicandonmez90@gmail.com

# Utilize Python Efficient in Docker Container
ENV PYTHONUNBUFFERED 1

# Install Python Dependencies
COPY requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install --upgrade pip \
    && pip install -r /requirements.txt
RUN apk del .tmp-build-deps

# Create Working Directory
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Create User
RUN adduser -D appuser
USER appuser

# copy entrypoint.sh
#COPY ./entrypoint.sh /app/entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
