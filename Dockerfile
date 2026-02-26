FROM python:3.12-slim

WORKDIR /app

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ api/
COPY identity/ identity/
COPY site/ site/

ENV ZORA_BACKEND=anthropic
ENV OLLAMA_HOST=http://localhost:11434
ENV OLLAMA_MODEL=zora-outer

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
