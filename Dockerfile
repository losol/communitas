FROM python:3.10-slim AS build

ENV POETRY_VERSION=1.1.13 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true  \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"\
    PATH="$POETRY_HOME/bin:$VENV_PATH/bin:/root/.local/bin:$PATH"

WORKDIR /app

RUN pip install --user "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY poetry.lock pyproject.toml ./
RUN poetry export --format requirements.txt --output /app/requirements.txt


FROM build as final
WORKDIR /app
COPY --from=build /app/requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run server
CMD gunicorn index:server
