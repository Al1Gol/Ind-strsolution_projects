FROM python:3.11.3
RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYCODE 1

WORKDIR /app/backend

COPY ./indsol_web /app/backend/

RUN pip install -r /app/backend/requirements.txt
RUN pip install gunicorn