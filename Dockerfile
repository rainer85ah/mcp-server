FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt update && apt install -y --no-install-recommends curl ca-certificates

WORKDIR /app
COPY . /app

RUN uv venv && uv pip install --system  --no-cache .

EXPOSE 8000
ENV ENV=production

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
