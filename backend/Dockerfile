FROM python:3.8

WORKDIR /code

ARG PORT=8055
ENV PORT=$PORT

ENV ES_URL=

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

ENTRYPOINT  uvicorn app.main:app --host 0.0.0.0 --port $PORT