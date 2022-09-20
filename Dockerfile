FROM python:3.10

WORKDIR /recipe-api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./api ./api

CMD["python", "./api/main.py"]
