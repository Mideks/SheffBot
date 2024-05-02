FROM python:3.9-slim
LABEL authors="mideks"

WORKDIR /app
COPY . .

CMD pip install -r requirements.txt
RUN ["python", "main.py"]