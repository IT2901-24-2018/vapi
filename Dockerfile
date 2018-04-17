FROM python:3
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip3 --no-cache-dir install -r requirements.txt
