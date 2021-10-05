FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev \
    build-essential libssl-dev libffi-dev python3-setuptools 

RUN apt-get install wget -y

WORKDIR /app

# 기본으로 동작할 파일 
ENV FLASK_APP=run.py

# 실행시 호스트 ip
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt

RUN pip3 install markupsafe==1.0.0

RUN pip3 install -r requirements.txt

EXPOSE 5000


