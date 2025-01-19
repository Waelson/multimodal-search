# Etapa 1: Construção da aplicação
FROM node:18-alpine AS builder

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do package.json e package-lock.json para instalar dependências
COPY package*.json ./

# Instala as dependências
RUN npm install

# Copia o restante dos arquivos da aplicação para o diretório de trabalho
COPY . .

# Compila a aplicação React em arquivos estáticos de produção
RUN npm run build

# Etapa 2: Configuração do servidor para servir os arquivos estáticos
FROM nginx:alpine

# Remove o arquivo de configuração padrão do Nginx
RUN rm -rf /usr/share/nginx/html/*

# Copia os arquivos compilados da etapa anterior para o diretório padrão do Nginx
COPY --from=builder /app/build /usr/share/nginx/html

# Exponha a porta usada pelo Nginx
EXPOSE 80

# Comando para iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]
