FROM python:3.9-slim

WORKDIR /app

RUN apt update && apt install -y git

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY app /app/app

ENV PYTHONPATH=/app

COPY scripts /app/scripts
RUN chmod +x scripts/nltk_dependencies.sh 
RUN scripts/nltk_dependencies.sh

CMD uvicorn app.main:app --host 0.0.0.0 --port 8000
