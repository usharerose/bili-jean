DockerfileFROM python:3.10-alpine3.20 AS builder

MAINTAINER Chaojie Yan

# Setup basic Linux packages
RUN apk update && \
    apk add --no-cache tini tzdata build-base libffi-dev make && \
    apk upgrade && \
    rm -rf /var/cache/apk/*

# Set workdir
WORKDIR /app/bili-jean/

COPY . .

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.8.3 \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # no virtual env need for container
    POETRY_VIRTUALENVS_CREATE=false

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$PATH"
# Add PYTHONPATH
ENV PYTHONPATH /app/bili-jean/

# install dependencies
RUN python -m pip install --no-cache --upgrade pip && \
    python -m pip install --no-cache poetry==${POETRY_VERSION} && \
    poetry install && \
    find /usr/local/ -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

FROM python:3.10-alpine3.20 AS dev

COPY --from=builder /etc/ /etc/
COPY --from=builder /usr/ /usr/
COPY --from=builder /app/bili-jean/ /app/bili-jean/
COPY --from=builder /sbin/ /sbin/

# Set workdir
WORKDIR /app/bili-jean/

# Tini is now available at /sbin/tini
ENTRYPOINT ["/sbin/tini", "--"]
