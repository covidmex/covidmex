FROM ubuntu:16.04

LABEL  maintainer="guillermoalvarado89@gmail.com"
LABEL maintainer="francisco.araya@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev libmysqlclient-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["manage.py", "run"]