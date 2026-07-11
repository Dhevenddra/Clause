FROM --platform=linux/amd64 python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY static ./static
COPY demo ./demo
EXPOSE 8000
# Render (and most PaaS) inject PORT; default to 8000 for local/docker-run parity.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
