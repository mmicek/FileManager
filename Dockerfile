# ===== Stage 1: Build =====
FROM python:3.13-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y curl build-essential \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.in-project true \
    && poetry install --no-root \
    && rm -rf ~/.cache/pypoetry/* ~/.cache/pip/*

COPY . /app/

# ===== Stage 2: Runtime =====
FROM python:3.13-slim
WORKDIR /app
ENV PYTHONPATH=$PYTHONPATH:/app

COPY --from=builder /app /app

# Install bash and Poetry for init.sh script
RUN apt-get update && apt-get install -y bash python3-pip \
    && python3 -m pip install poetry \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"
COPY init.sh /app/init.sh
RUN chmod +x /app/init.sh

EXPOSE 8000
ENTRYPOINT ["bash", "/app/init.sh"]
