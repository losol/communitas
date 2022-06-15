FROM python:3.10-slim AS build

ENV POETRY_VERSION=1.1.13

WORKDIR /app

RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml ./
RUN python -m venv /app/venv

RUN poetry export --without-hashes --format requirements.txt --output /app/requirements.txt


FROM python:3.10-slim AS prod

ENV PATH /app/venv/bin:$PATH \
    PYTHONPATH=/app

WORKDIR /app

COPY --from=build /app/requirements.txt . 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run server
EXPOSE ${PORT:-8000}
CMD gunicorn --bind 0.0.0.0:${PORT:-8000} index:server
