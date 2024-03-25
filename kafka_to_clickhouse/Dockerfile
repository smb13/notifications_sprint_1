FROM python:3.11
LABEL maintainer="budaev.digital@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/src/app"

RUN mkdir -p /src/app

RUN groupadd -r web && useradd -d /src/app -r -g web web \
    && chown web:web -R /src/app

WORKDIR /src/app

COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .

CMD python ./main.py
