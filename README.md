# Sistema de Busca Multimodal

![technology Python](https://img.shields.io/badge/technology-Python-blue.svg)  ![technology JavaScript](https://img.shields.io/badge/technology-JavaScript-blue.svg) ![technology Postgres](https://img.shields.io/badge/technology-Postgres-green.svg) ![technology Milvus](https://img.shields.io/badge/technology-Milvus-green.svg) ![technology Flask](https://img.shields.io/badge/technology-Flask-orange.svg) ![technology PyTorch](https://img.shields.io/badge/technology-PyTorch-orange.svg) ![technology Transformer](https://img.shields.io/badge/technology-Transformer-orange.svg) ![technology React](https://img.shields.io/badge/technology-React-orange.svg)

Este repositório contem a implementação de um **sistema de busca multimodal**, projetado para simular um mecanismo avançado de busca de produtos em um e-commerce fictício utilizando texto, imagens, ou a combinação de ambos. O sistema permite realizar consultas eficientes, proporcionando uma experiência mais interativa.  

## Arquitetura da Solução
![Architecture](documentation/architecture-embedding.png)

### Componentes da Arquitetura
| **Componente**        | **Descrição**                                                    |
|-----------------------|------------------------------------------------------------------|
| product-search-web    | Interface usada por usuários de e-commerce consultar os produtos |
| product-search-api    | Backend responsável por buscar produtos                          |
| multimodal-search-api | TODO                                                             |
| multimodal-indexer    | TODO                                                             |

### Tecnologias Utilizadas
| **Categoria**         | **Ferramenta/Descrição**                                                                 |
|------------------------|------------------------------------------------------------------------------------------|
| **Linguagem**          | Python                                                                                  |
| **Bibliotecas**        | Flask, Torch, Transformers, Pillow, Pymilvus                                            |
| **Banco de Dados**     | Milvus (Vector Database), Postgres                                                      |
| **Dataset**            | [E-commerce Product Images](https://www.kaggle.com/datasets/vikashrajluhaniwal/fashion-images) (disponível no Kaggle) |


### Executando

A aplicação está configurada para ser executada com Docker Compose. Siga os seguintes passos:

1. **Clone o repositório**

```bash
git clone https://github.com/Waelson/multimodal-search.git
cd multimodal-search
```

2. **Suba toda a stack**

```bash
docker-compose up --build
```

3. **Acessando a aplicação**
   - Digite a URL http://localhost:3001/ no browser
   - Clique no ícone da `câmera` para selecionar uma imagem. Lembre-se: a base de dados contém imagens de tênis e calçados masculino e feminino, além de roupas infantis masculinas e femininas. Portanto, ao realizar a consulta selecione imagens nessas categorias. 

## Como a Aplicação se Parece

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