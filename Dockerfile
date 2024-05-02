FROM python:3.9-slim
LABEL authors="mideks"

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
CMD ["python", "main.py"]