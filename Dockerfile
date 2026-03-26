FROM python:3.12-slim

RUN pip install --no-cache-dir uv

RUN useradd -m -u 1000 appuser

ENV HOME=/home/appuser

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY main.py .

# FIX: give appuser ownership of cache + app
RUN mkdir -p /home/appuser/.cache/uv \
    && chown -R appuser:appuser /home/appuser /app

USER appuser

ENTRYPOINT ["sh", "-c", "while true; do uv run main.py; sleep 14400; done"]
