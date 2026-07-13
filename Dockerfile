FROM python:3.7-slim

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir /app/
COPY ./src/ /app/

RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin appuser \
    && chown -R appuser:appuser /app

WORKDIR /app
USER appuser

CMD ["python", "/app/main.py"]

EXPOSE 8081

