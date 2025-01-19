# Sistema de Busca Multimodal

![technology Python](https://img.shields.io/badge/technology-Python-blue.svg)  ![technology JavaScript](https://img.shields.io/badge/technology-JavaScript-orange.svg) ![technology MachineLearning](https://img.shields.io/badge/technology-MachineLearning-green.svg) 

Este repositório contem a implementação de um **sistema de busca multimodal**, projetado para simular um mecanismo avançado de busca de produtos em um e-commerce fictício utilizando texto, imagens, ou a combinação de ambos. O sistema permite realizar consultas eficientes, proporcionando uma experiência mais interativa.  

## Arquitetura
![Architecture](documentation/architecture-embedding.png)

### Componentes
| **Componente**        | **Descrição**                                                                                         |
|-----------------------|-------------------------------------------------------------------------------------------------------|
| product-search-web    | Interface usada por usuários do e-commerce para consultar os produtos                                 |
| product-search-api    | Backend responsável por buscar produtos                                                               |
| multimodal-search-api | A partir de um texto e/ou imagem, buscar por itens similares na base de dados vetorial                |
| multimodal-indexer    | Job usado para ler o dataset (csv e imagens), gerar o embedding e inseri-lo na base de dados vetorial |
| Postgres              | Armazena todos os dados dos produtos como: nome, URL da image, categoria e outras características     |
| Milvus                | Armazena o embedding (vetor) de cada produto, juntamente com seu respectivo ID                        |

### Tecnologias
| **Categoria**         | **Ferramenta/Descrição**                                                                                              |
|------------------------|-----------------------------------------------------------------------------------------------------------------------|
| **Linguagem**          | Python, Java Script                                                                                                   |
| **Bibliotecas**        | Flask, Torch, Transformers, Pillow, Pymilvus, React                                                                   |
| **Banco de Dados**     | [Milvus (Vector Database)](https://milvus.io/), Postgres                                                                                |
| **Dataset**            | [E-commerce Product Images](https://www.kaggle.com/datasets/vikashrajluhaniwal/fashion-images) (disponível no Kaggle) |


## Instalação

A aplicação está configurada para ser executada com Docker Compose. Siga os seguintes passos:

Pré-requisitos:
- Python 3.11 ou superior
- Node 20.12 ou superior (para executar projeto localmente)

1. **Clona o repositório**

```bash
git clone https://github.com/Waelson/multimodal-search.git
cd multimodal-search
```

2. **Inicializa a stack**

```bash
docker-compose up --build
```

3. **Prepara a indexação do dataset**
- Cria um Virtual Environment do Python

```bash
python -m venv my-venv
```

- Ativa o Virtual Environment

```bash
source my-venv/bin/activate
```
- Instala as dependências

```bash
pip install -r requirements.txt
```

- Executa o processo de indexação do dataset

```bash
cd projects/multimodal-indexer
python app.py
```

4. **Acessa a aplicação**
- Digite a URL http://localhost:3001/ no browser
- Clique no ícone da `câmera` para selecionar uma imagem. Lembre-se: a base de dados contém imagens de tênis e calçados masculino e feminino, além de roupas infantis masculinas e femininas. Portanto, ao realizar a consulta selecione imagens nessas categorias. 

## Interface de Consulta de Produtos

![Screen](documentation/app-screen.png)
   
## Teoria

### O que é busca multimodal?
São buscas que combinam diferentes tipos de dados (ou "modalidades") para encontrar resultados. Por exemplo, você pode buscar com uma imagem e um texto ao mesmo tempo, ou usar áudio e vídeo como entrada para encontrar conteúdos relacionados.

### Que tipos de problema resolve?

1. **E-Commerce**
   - **Busca de produtos por imagem e texto:**
      - O cliente pode carregar a foto de um produto e adicionar um texto como "sapato vermelho tamanho 40", e o sistema encontrará itens que correspondem à imagem e à descrição.
   - **Recomendações personalizadas:**
      - Sugerir produtos relacionados a uma combinação de fotos enviadas e histórico de pesquisa textual.
2. **Saúde**
   - **Busca por diagnósticos médicos:**
      - Médicos podem combinar imagens de exames (como raios-X ou ressonâncias) com descrições textuais de sintomas para encontrar diagnósticos ou casos similares.
3. **Educacional**
   - **Busca em conteúdos educacionais:**
      - Estudantes podem combinar texto (ex.: "Teoria da Relatividade") com gráficos ou diagramas, encontrando explicações que relacionam ambas as modalidades.


## Como o Vector Database pode nos ajudar?

### O que são Vector Databases?

É um tipo de banco de dados projetado para armazenar e buscar vetores de alta dimensão, que são representações numéricas geradas por algoritmos de aprendizado de máquina. Esses vetores capturam características semânticas de dados complexos, como textos, imagens, áudios ou vídeos.

Os vetores são armazenados no banco e podem ser consultados com base em similaridade (em vez de buscas exatas), usando métricas como:
- Similaridade de cosseno
- Distância Euclidiana
- Distância de Manhattan