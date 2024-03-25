FROM python:3.12.2
LABEL maintainer="safeflat@gmail.com"

RUN apt-get update && apt-get install -y --no-install-recommends curl nano gcc musl-dev && apt-get clean

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH '/src'

WORKDIR /src/

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt

COPY . .

CMD python