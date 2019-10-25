FROM python:3.7
RUN pip install pipenv
WORKDIR /app
COPY . /app
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt
RUN python3 ./src/main.py update

CMD python3 ./src/main.py
