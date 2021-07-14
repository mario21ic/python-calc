FROM python:3.7-slim

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir /app/
COPY ./src/ /app/

WORKDIR /app

CMD ["python", "/app/main.py"]

EXPOSE 8081

