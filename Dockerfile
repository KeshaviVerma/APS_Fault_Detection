FROM python:3.10-slim

RUN apt-get update -y && apt-get install -y awscli

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]