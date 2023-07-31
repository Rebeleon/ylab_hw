FROM python:3.10-slim

WORKDIR /api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
