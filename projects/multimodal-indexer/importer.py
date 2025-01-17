from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import torchvision.transforms as transforms
import csv
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Conectar ao Milvus
try:
    logging.info("Conectando ao Milvus...")
    connections.connect(host="localhost", port="19530")
    logging.info("Conexão com Milvus bem-sucedida.")
except Exception as e:
    logging.error(f"Erro ao conectar ao Milvus: {e}")
    raise

# Definir o esquema da coleção no Milvus
try:
    logging.info("Definindo esquema da coleção no Milvus...")
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=512),
    ]
    schema = CollectionSchema(fields, description="Catálogo multimodal de produtos")
    collection = Collection(name="multimodal_product_catalog", schema=schema)
    logging.info("Esquema da coleção definido com sucesso.")
except Exception as e:
    logging.error(f"Erro ao definir esquema da coleção: {e}")
    raise

# Carregar modelos
try:
    logging.info("Carregando modelo CLIP diretamente...")
    clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    logging.info("Modelo CLIP carregado com sucesso.")
except Exception as e:
    logging.error(f"Erro ao carregar modelo CLIP: {e}")
    raise

# Ler dados do arquivo CSV
csv_file_path = "../../data/fashion.csv"
products = []
try:
    logging.info(f"Lendo dados do arquivo CSV: {csv_file_path}...")
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append({
                "id": int(row["ProductId"]),
                "text": f"{row['Gender']} {row['Category']} {row['SubCategory']} {row['ProductType']} {row['Colour']} {row['Usage']} {row['ProductTitle']}",
                "image_path": os.path.join("/Users/waelson/Documents/workspace/multimodal-search/data/images", row["Image"])
            })
    logging.info(f"{len(products)} produtos carregados do arquivo CSV.")
except Exception as e:
    logging.error(f"Erro ao ler o arquivo CSV: {e}")
    raise

# Gerar embeddings multimodais
embeddings = []
for product in products:
    try:
        logging.info(f"Gerando embedding para o produto ID: {product['id']}...")

        # Gerar embedding de texto
        text_inputs = clip_processor(text=product["text"], return_tensors="pt", padding=True)
        with torch.no_grad():
            text_embedding = clip_model.get_text_features(**text_inputs).squeeze().numpy()

        # Gerar embedding de imagem
        try:
            image = Image.open(product["image_path"]).convert("RGB")
            image_inputs = clip_processor(images=image, return_tensors="pt")
            with torch.no_grad():
                image_embedding = clip_model.get_image_features(**image_inputs).squeeze().numpy()
        except FileNotFoundError:
            logging.warning(f"Imagem não encontrada: {product['image_path']}, usando apenas embedding de texto.")
            image_embedding = text_embedding  # Fallback para texto se a imagem não existir

        # Combinar os embeddings (média simples)
        combined_embedding = (text_embedding + image_embedding) / 2
        embeddings.append(combined_embedding)
    except Exception as e:
        logging.error(f"Erro ao gerar embedding para o produto ID {product['id']}: {e}")
        raise

# Inserir dados no Milvus
try:
    logging.info("Inserindo dados no Milvus...")
    ids = [product["id"] for product in products]
    collection.insert([ids, embeddings])
    logging.info("Dados inseridos com sucesso no Milvus.")
except Exception as e:
    logging.error(f"Erro ao inserir dados no Milvus: {e}")
    raise

# Criar índice para busca
try:
    logging.info("Criando índice para busca no Milvus...")
    collection.create_index(field_name="embedding", index_params={"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 128}})
    logging.info("Índice criado com sucesso.")
except Exception as e:
    logging.error(f"Erro ao criar índice no Milvus: {e}")
    raise
