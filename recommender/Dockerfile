FROM python:3.8

WORKDIR /usr/src/app

RUN apt-get update
RUN apt install gcc
RUN pip install --upgrade pip 
RUN pip install cython
RUN pip install numpy
RUN pip install --no-cache-dir rankfm

COPY . .
ENTRYPOINT ["python", "main.py"]