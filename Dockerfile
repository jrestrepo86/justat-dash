FROM python:3.12.4-alpine3.20

ENV DASH_DEBUG_MODE=True

COPY ./app /app

WORKDIR /app

RUN set -ex && \
    pip install -r requirements.txt

CMD ["python3", "app.py"]
