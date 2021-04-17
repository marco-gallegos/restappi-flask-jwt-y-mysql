FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add gcc musl-dev linux-headers build-base alpine-sdk

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python src/app.py