from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import psycopg2
import os

# Configurar Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS para todos os endpoints

# Variáveis de ambiente para configurar PostgreSQL e endpoint multimodal
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ecommerce")
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
MULTIMODAL_ENDPOINT = os.getenv("MULTIMODAL_ENDPOINT", "http://localhost:5001/search/multimodal")

# Configurar conexão com PostgreSQL
def get_postgres_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

# Endpoint para buscar por texto ou imagem
@app.route("/api/v1/search", methods=["POST"])
def search():
    try:
        # Verificar parâmetros recebidos
        query_text = request.form.get("text")
        image_file = request.files.get("image")

        if not query_text and not image_file:
            return jsonify({"error": "Texto ou imagem são obrigatórios."}), 400

        # Enviar consulta para o endpoint multimodal
        files = {}
        if query_text:
            files["text"] = (None, query_text)
        if image_file:
            files["image"] = (image_file.filename, image_file.stream, image_file.content_type)

        multimodal_response = requests.post(MULTIMODAL_ENDPOINT, files=files)
        if multimodal_response.status_code != 200:
            return jsonify({"error": "Erro ao consultar o endpoint multimodal.",
                            "details": multimodal_response.text}), 500

        # Obter IDs retornados pelo endpoint multimodal e filtrar por score
        multimodal_data = multimodal_response.json()
        filtered_data = [item for item in multimodal_data if item["score"] <= 50]

        if not filtered_data:
            return jsonify({"message": "Nenhum produto encontrado com score <= 50."}), 404

        product_ids = [str(item["id"]) for item in filtered_data]

        # Consultar produtos no PostgreSQL
        query = f"SELECT * FROM products WHERE product_id IN ({','.join(product_ids)});"
        connection = get_postgres_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        products = cursor.fetchall()

        # Mapear resultados para um formato JSON
        product_results = []
        for product in products:
            product_results.append({
                "product_id": product[0],
                "gender": product[1],
                "category": product[2],
                "sub_category": product[3],
                "product_type": product[4],
                "colour": product[5],
                "usage": product[6],
                "product_title": product[7],
                "image": f"/images/{product[8]}",
                "image_url": product[9]
            })

        cursor.close()
        connection.close()

        return jsonify(product_results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Executar a aplicação Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
