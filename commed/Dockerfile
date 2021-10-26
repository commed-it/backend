FROM python:3.10-slim

ENV PYTHONDOTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get install gcc libpq-dev g++ -y

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_lg

COPY . /app
