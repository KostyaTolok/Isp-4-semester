FROM python:3.8.5-slim-buster

ENV PYTHONUNBUFFERED=1
WORKDIR usr/src/Lab3
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
