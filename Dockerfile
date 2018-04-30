FROM python:3
ENV PYTHONUNBUFFERED 1

# GeoDjango!
RUN apt-get --assume-yes update; apt-get --assume-yes install binutils libproj-dev gdal-bin

WORKDIR /vapi

COPY requirements.txt /vapi/requirements.txt

RUN pip3 --no-cache-dir install -r requirements.txt
