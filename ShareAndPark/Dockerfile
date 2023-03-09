

# pull official base image
FROM python:3.8

MAINTAINER XanderMoroz <moroz070688@gmail.com>
# set work directory

COPY ./ShareAndPark /srv/www/ShareAndPark
WORKDIR /srv/www/ShareAndPark
#WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


EXPOSE 5000

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

