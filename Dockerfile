FROM python:3.8-buster
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
COPY . .
ARG name

RUN apt-get update
RUN pip install --upgrade pip
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN ["python","manage.py","migrate"]
RUN ["gunicorn","mlAmeri.wsgi:application","--bind","0.0.0.0:8000"]