

# pull official base image
FROM python:3.8

MAINTAINER XanderMoroz <moroz070688@gmail.com>
# set work directory

COPY ../../ShareAndPark /srv/www/ShareAndPark
WORKDIR /srv/www/ShareAndPark
#WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


EXPOSE 5000

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    python-all-dev \
    libpq-dev \
    libgeos-dev \
    wget \
    curl \
    sqlite3 \
    cmake \
    libtiff-dev \
    libsqlite3-dev \
    libcurl4-openssl-dev \
    pkg-config


# This is just an example with hard-coded paths/uris and no cleanup...
RUN curl https://download.osgeo.org/proj/proj-8.2.1.tar.gz | tar -xz &&\
    cd proj-8.2.1 &&\
    mkdir build &&\
    cd build && \
    cmake .. &&\
    make && \
    make install

RUN wget http://download.osgeo.org/gdal/3.4.0/gdal-3.4.0.tar.gz
RUN tar xvfz gdal-3.4.0.tar.gz
WORKDIR ./gdal-3.4.0
RUN ./configure --with-python --with-pg --with-geos &&\
    make && \
    make install && \
    ldconfig
#RUN apt-get update && apt-get install gdal-bin

WORKDIR /srv/www/ShareAndPark

# install dependencies
RUN pip install --upgrade pip
COPY ../../ShareAndPark/requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY ../../ShareAndPark .

