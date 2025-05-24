FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt update && apt install -y --no-install-recommends curl ca-certificates

WORKDIR /app
COPY . /app

RUN uv venv && uv pip install --system .

EXPOSE 8000
ENV ENV=production

CMD ["python", "main.py"]