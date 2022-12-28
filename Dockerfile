FROM python:3.11-slim

WORKDIR /code

COPY ./requirements/app.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src/ /code/

RUN mkdir /data/
RUN mkdir /logs/

WORKDIR /code/