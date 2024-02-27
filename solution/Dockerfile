FROM python:3.12.1-alpine3.19

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .

ENV SERVER_PORT=8080

EXPOSE $SERVER_PORT

CMD poetry run uvicorn --factory app:create_app --host 0.0.0.0 --port $SERVER_PORT