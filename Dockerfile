# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN apt-get install -y ttf-mscorefonts-installer fontconfig

CMD [ "python3", "uznypa.py", "--host=0.0.0.0"]
