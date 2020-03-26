FROM ubuntu:16.04

LABEL  maintainer="guillermoalvarado89@gmail.com"
LABEL maintainer="francisco.araya@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

ENV FLASK_ENV development
ENV FLASK_APP covidmex

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD flask run --host=0.0.0.0