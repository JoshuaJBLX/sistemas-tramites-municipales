FROM python:3.13-slim

WORKDIR /app

# Dependencias.
# 1) torch CPU-only primero: la rueda CUDA por defecto pesa ~2.5GB y no hace
#    falta en la nube (BGE-M3 corre en CPU, EMBEDDING_DEVICE=cpu).
# 2) Luego requirements.txt completo (torch ya satisface a sentence-transformers).
COPY requirements.txt .
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

# Pre-descarga el modelo BGE-M3 (~2.3GB) dentro de la imagen para que la
# primera consulta no pague la bajada desde HuggingFace. Capa separada:
# cambios de código (COPY . .) no invalidan esta caché del builder.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-m3')"

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8080

# Fly.io inyecta PORT (http_service.internal_port = 8080 en fly.toml)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
