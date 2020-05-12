FROM python:3.7-slim-stretch
RUN pip install pipenv
WORKDIR /app
COPY . /app
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt
RUN mkdir -p /var/lib/pymdb

CMD python3 ./src/main.py
