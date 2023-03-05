FROM python:3.10-alpine

RUN apk add --no-cache --update \
    build-base \
    libffi-dev \
    openssl-dev

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]