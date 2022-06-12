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

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

ENV PATH="/home/appuser/.local/bin:$PATH"

COPY --from=build /app/requirements.txt . 
RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .

# Run server
CMD gunicorn index:server
