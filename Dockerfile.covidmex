FROM tiangolo/meinheld-gunicorn:python2.7

ENV  MODULE_NAME="covidmex.wsgi" 

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app