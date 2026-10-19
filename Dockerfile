# ==============================================================================
# Etapa 1: Builder (Instalación de dependencias de Python y SWI-Prolog)
# ==============================================================================
FROM python:3.12-slim AS builder

WORKDIR /build

# Instalar dependencias de compilación mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ==============================================================================
# Etapa 2: Runner / Producción (Imagen final ligera y segura)
# ==============================================================================
FROM python:3.12-slim AS runner

WORKDIR /app

# Instalar binario nativo de SWI-Prolog y curl para Healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    swi-prolog \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no privilegiado para seguridad
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/knowledge && \
    chown -R appuser:appuser /app

# Copiar paquetes instalados desde el builder
COPY --from=builder /root/.local /home/appuser/.local

# Configurar variables de entorno para PATH y Python
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true

# Copiar el código fuente del proyecto
COPY --chown=appuser:appuser . /app

# Cambiar al usuario no privilegiado
USER appuser

# Exponer el puerto predeterminado de Streamlit
EXPOSE 8501

# Healthcheck oficial de Streamlit
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Comando de inicio del servidor web
CMD ["streamlit", "run", "app.py"]
