RUN python:3.10.12
RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYCODE 1

WORKDIR /app/backend

COPY ./indsol_web /app/backend/

RUN pip install -r /app/backend/requirements.txt
RUN pip install gunicorn