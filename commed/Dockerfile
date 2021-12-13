FROM python:3.9-slim

ENV PYTHONDOTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get install gcc libpq-dev g++ -y

RUN mkdir /app

WORKDIR /app

RUN pip install spacy==3.1.3

RUN python -m spacy download en_core_web_lg

COPY requirements.txt /app/

RUN pip install -r requirements.txt


COPY . /app
