# pull official base image
FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip pipenv
COPY ./Pipfile /usr/src/app/Pipfile
RUN sed -i 's/psycopg2/psycopg2-binary/g' ./Pipfile
RUN pipenv install

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
