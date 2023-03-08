

# pull official base image
FROM python:3.8

MAINTAINER XanderMoroz <moroz070688@gmail.com>
# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN apk update && apk upgrade
#RUN apk add --no-cache bash git gcc
#RUN apk update && apk add python3-dev gcc libc-dev libffi-dev
EXPOSE 5000

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

