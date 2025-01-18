# Sistema de Busca Multimodal

Esse repositório contém a implementação de um sistema de busca multimodal que simula um mecânismo de busca de produtos por texto e/ou imagem.  

## Arquitetura da Solução
![Architecture](documentation/architecture-embedding.png)

### Componentes
| **Componente**        | **Descrição**                                                    |
|-----------------------|------------------------------------------------------------------|
| product-search-web    | Interface usada por usuários de e-commerce consultar os produtos |
| product-search-api    | Backend responsável por buscar produtos                          |
| multimodal-search-api | TODO                                                             |
| multimodal-indexer    | TODO                                                             |

### Ferramentas utilizadas
1. **Linguagem** 
   - Python
2. **Bibliotecas**
   - Flask
   - Torch
   - Transformer
   - Pillow
   - Pymilvus
3. **Banco de Dados**
   - Milvus (Vector Database)
   - Postgres
4. Dataset
   - E-commerce Product Images (disponível no Kaggle em: https://www.kaggle.com/datasets/vikashrajluhaniwal/fashion-images)


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