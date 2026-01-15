ARG PYTHON_VERSION=3.13.5
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN --mount=type=cache,id=pip-cache,target=/root/.cache/pip \
    python -m pip install --no-cache-dir -r requirements.txt

COPY . .
USER appuser

EXPOSE 8000

# Run the application.
CMD ["python", "server.py"]
