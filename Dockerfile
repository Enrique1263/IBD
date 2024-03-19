
FROM python:3.8-slim

WORKDIR /usr/src/app

COPY ./collector.py ./collector.py

RUN pip install --no-cache-dir requests pymongo newsapi-python

CMD ["python", "-u", "./collector.py"]
