import os
from flask import Flask, request, jsonify
from pymilvus import connections, Collection
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configurar Flask
app = Flask(__name__)

# Variáveis de ambiente com valores padrão
MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")

# Conectar ao Milvus
try:
    logging.info(f"Conectando ao Milvus em {MILVUS_HOST}:{MILVUS_PORT}...")
    connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
    collection = Collection("multimodal_product_catalog")
    logging.info("Conexão com Milvus bem-sucedida.")

    # Carregar a coleção na memória
    logging.info("Carregando coleção no Milvus...")
    collection.load()
    logging.info("Coleção carregada com sucesso.")
except Exception as e:
    logging.error(f"Erro ao conectar ou carregar coleção no Milvus: {e}")
    raise

# Carregar modelo CLIP
try:
    logging.info("Carregando modelo CLIP...")
    clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    logging.info("Modelo CLIP carregado com sucesso.")
except Exception as e:
    logging.error(f"Erro ao carregar modelo CLIP: {e}")
    raise

# Função para buscar embeddings no Milvus
def search_in_milvus(embedding, top_k=10):
    try:
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = collection.search(
            data=[embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["id"],  # Garantir que o campo ID seja retornado
        )
        return [
            {"id": hit.entity.get("id"), "score": hit.distance}
            for hit in results[0]
        ]
    except Exception as e:
        logging.error(f"Erro ao buscar no Milvus: {e}")
        raise

# Endpoint para buscar por texto
@app.route("/search/text", methods=["POST"])
def search_by_text():
    try:
        data = request.json
        query_text = data.get("text")

        if not query_text:
            return jsonify({"error": "Texto de busca é obrigatório."}), 400

        # Gerar embedding de texto
        text_inputs = clip_processor(text=query_text, return_tensors="pt", padding=True)
        with torch.no_grad():
            text_embedding = clip_model.get_text_features(**text_inputs).squeeze().numpy()

        # Buscar no Milvus
        results = search_in_milvus(text_embedding)
        return jsonify(results)
    except Exception as e:
        logging.error(f"Erro ao buscar por texto: {e}")
        return jsonify({"error": str(e)}), 500

# Endpoint para buscar por imagem
@app.route("/search/image", methods=["POST"])
def search_by_image():
    try:
        if "image" not in request.files:
            return jsonify({"error": "Imagem é obrigatória."}), 400

        image_file = request.files["image"]
        image = Image.open(image_file).convert("RGB")

        # Gerar embedding de imagem
        image_inputs = clip_processor(images=image, return_tensors="pt")
        with torch.no_grad():
            image_embedding = clip_model.get_image_features(**image_inputs).squeeze().numpy()

        # Buscar no Milvus
        results = search_in_milvus(image_embedding)
        return jsonify(results)
    except Exception as e:
        logging.error(f"Erro ao buscar por imagem: {e}")
        return jsonify({"error": str(e)}), 500

# Endpoint para buscar por texto e imagem
@app.route("/search/multimodal", methods=["POST"])
def search_by_text_and_image():
    try:
        query_text = request.form.get("text")
        image_file = request.files.get("image")

        if not query_text and not image_file:
            return jsonify({"error": "É necessário enviar pelo menos texto ou imagem para busca."}), 400

        # Gerar embedding de texto, se fornecido
        if query_text:
            text_inputs = clip_processor(text=query_text, return_tensors="pt", padding=True)
            with torch.no_grad():
                text_embedding = clip_model.get_text_features(**text_inputs).squeeze().numpy()
        else:
            text_embedding = None

        # Gerar embedding de imagem, se fornecida
        if image_file:
            image = Image.open(image_file).convert("RGB")
            image_inputs = clip_processor(images=image, return_tensors="pt")
            with torch.no_grad():
                image_embedding = clip_model.get_image_features(**image_inputs).squeeze().numpy()
        else:
            image_embedding = None

        # Combinar embeddings
        if text_embedding is not None and image_embedding is not None:
            combined_embedding = (text_embedding + image_embedding) / 2
        elif text_embedding is not None:
            combined_embedding = text_embedding
        elif image_embedding is not None:
            combined_embedding = image_embedding
        else:
            return jsonify({"error": "Erro ao gerar embeddings."}), 500

        # Buscar no Milvus
        results = search_in_milvus(combined_embedding)
        return jsonify(results)
    except Exception as e:
        logging.error(f"Erro ao buscar por texto e imagem: {e}")
        return jsonify({"error": str(e)}), 500


# Executar a aplicação Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
