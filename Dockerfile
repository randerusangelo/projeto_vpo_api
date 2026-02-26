FROM python:3.12-slim-bookworm

RUN rm -rf /var/lib/apt/lists/*

# Diretório da aplicação
WORKDIR /app
COPY gitclone/ .
 
# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt
 
# Variáveis de ambiente
ENV FLASK_APP=api.py \
    PYTHONPATH=/app
 
# Ponto de entrada com Waitress
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "api:app"]