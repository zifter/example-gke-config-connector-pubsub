FROM europe-central2-docker.pkg.dev/maintenance-internal-services/docker-registry/external-images/python:3.10.7-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends curl 

# set work directory
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# copy project
COPY main.py main.py

ENTRYPOINT [""]
