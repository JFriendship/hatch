FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

# Install cpu only pytorch before installing other dependencies
RUN pip install --no-cache-dir torch==2.12.1 \
    --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

# Creates a user and provides a place for caching hugging face files
RUN useradd -m appuser && \
    mkdir -p /home/appuser/.cache/huggingface/hub && \
    chown -R appuser:appuser /home/appuser/.cache

# Copies app files into the docker image and assigns ownership to the appuser
COPY --chown=appuser:appuser app/ ./app/
    
USER appuser

EXPOSE 8000


CMD [\
  "uvicorn",\
  "app.main:app",\
#   "--reload",\
  "--host",\
  "0.0.0.0",\
  "--port",\
  "8000"\
]
