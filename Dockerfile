FROM python:3-alpine3.15

WORKDIR /app

COPY . /app

RUN apk add --no-cache build-base linux-headers postgresql-dev

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD python3 app.py