FROM ubuntu

WORKDIR /app
ADD . /app

RUN apt-get update
RUN apt-get install -y libmysqlclient-dev python-dev python-pip

RUN pip install -r requirements/dev.txt

RUN pip install -U pip wheel
