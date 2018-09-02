FROM python:3

WORKDIR code

RUN apt-get update && apt-get install -y \
    software-properties-common
#RUN apt-get install -y python3-pip
#RUN apt-get install -y python-setuptools
RUN apt-get install -y libevent-dev

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN rm requirements.txt
