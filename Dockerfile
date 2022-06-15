################
# Stage: Build #
################

FROM python:3.10-slim AS build

ENV POETRY_VERSION=1.1.13

WORKDIR /app

# Export poetry dependencies to file
RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml ./
RUN python -m venv /app/venv
RUN poetry export --without-hashes --format requirements.txt --output /app/requirements.txt

#####################
# Stage: Production #
#####################
FROM python:3.10-slim AS prod

ENV PYTHONPATH=/app

WORKDIR /app

# Create a non-root user to run the web server
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
ENV PATH="/home/appuser/.local/bin:$PATH"

# Copy requirements from build stage, and install them
COPY --from=build /app/requirements.txt . 
RUN pip install --user --no-cache-dir -r requirements.txt

COPY . .

# Run server
EXPOSE ${PORT:-8000}
CMD gunicorn --bind 0.0.0.0:${PORT:-8000} index:server
