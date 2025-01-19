# Usar uma imagem base do Python
FROM python:3.11-slim

# Criar o diretório da aplicação
WORKDIR /app

# Copiar os arquivos da aplicação para o contêiner
COPY . /app

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta usada pela aplicação
EXPOSE 8080

# Comando para rodar a aplicação
CMD ["python", "app.py"]
