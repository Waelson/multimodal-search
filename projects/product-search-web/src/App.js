import React, { useState } from "react";
import axios from "axios";

function App() {
  const [searchText, setSearchText] = useState("");
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false); // Estado de carregamento
  const [errorMessage, setErrorMessage] = useState(""); // Estado para mensagens de erro
  const [imageLoading, setImageLoading] = useState({}); // Controle de carregamento das imagens

  const handleSearch = async () => {
    const formData = new FormData();
    if (searchText) formData.append("text", searchText);
    if (imageFile) formData.append("image", imageFile);

    setLoading(true); // Ativa o estado de carregamento
    setResults([]); // Limpa os resultados anteriores
    setErrorMessage(""); // Limpa mensagens de erro

    try {
      const response = await axios.post("http://localhost:8080/api/v1/search", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setResults(response.data); // Supondo que a API retorna um array de objetos com { id, image_url, product_title }
    } catch (error) {
      console.error("Erro ao buscar:", error);
      if (error.response && error.response.status === 404) {
        setErrorMessage("Nenhum produto encontrado para os critérios de busca.");
      } else {
        setErrorMessage("Erro ao processar a solicitação. Tente novamente mais tarde.");
      }
    } finally {
      setLoading(false); // Desativa o estado de carregamento
    }
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (!file) {
      return; // Nenhum arquivo foi selecionado
    }
    setImageFile(file);
    setImagePreview(URL.createObjectURL(file)); // Criar um link para pré-visualização da imagem
  };

  const handleRemoveImage = () => {
    setImageFile(null);
    setImagePreview(null);
  };

  const handleClear = () => {
    setSearchText("");
    setImageFile(null);
    setImagePreview(null);
    setResults([]);
    setErrorMessage(""); // Limpa mensagens de erro
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSearch(); // Realiza a pesquisa ao pressionar Enter
    }
  };

  const defaultImage = "data:image/svg+xml;base64," + // Imagem cinza clara em base64
      btoa(
          `<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><rect width="200" height="200" fill="#d3d3d3"/></svg>`
      );

  const handleImageLoad = (id) => {
    setImageLoading((prevState) => ({ ...prevState, [id]: false }));
  };

  const handleImageError = (id) => {
    setImageLoading((prevState) => ({ ...prevState, [id]: false }));
  };

  return (
      <div style={styles.container}>
        <h1 style={styles.title}>Multimodal Search</h1>
        <div style={styles.searchContainer}>
          <input
              type="text"
              placeholder="Digite sua busca..."
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              onKeyDown={handleKeyDown} // Escuta o evento de pressionar tecla
              style={styles.input}
          />
          <div style={styles.imageUploadContainer}>
            <label htmlFor="upload-image" style={styles.icon}>
              📷
            </label>
            <input
                id="upload-image"
                type="file"
                accept="image/*"
                onChange={handleImageChange}
                style={{ display: "none" }}
            />
            {imagePreview && (
                <div style={styles.previewContainer}>
                  <img src={imagePreview} alt="Preview" style={styles.imagePreview} />
                  <div style={styles.removeIcon} onClick={handleRemoveImage}>
                    ✖
                  </div>
                </div>
            )}
          </div>
        </div>
        <div style={styles.buttonContainer}>
          <button onClick={handleClear} style={styles.clearButton}>
            Limpar
          </button>
          <button onClick={handleSearch} style={styles.button}>
            Pesquisar
          </button>
        </div>
        {loading && <div style={styles.loading}>Carregando...</div>} {/* Exibe mensagem de carregamento */}
        {errorMessage && <div style={styles.errorMessage}>{errorMessage}</div>} {/* Exibe mensagem de erro */}
        <div style={styles.resultsContainer}>
          {results.map((result) => (
              <div key={result.id} style={styles.resultItem}>
                {imageLoading[result.id] && <div style={styles.imageLoading}>Carregando...</div>}
                <img
                    src={result.image_url || defaultImage}
                    alt={result.product_title}
                    style={styles.resultImage}
                    onLoad={() => handleImageLoad(result.id)}
                    onError={(e) => {
                      handleImageError(result.id);
                      e.target.src = defaultImage;
                    }}
                />
                <p>{result.product_title}</p>
              </div>
          ))}
        </div>
      </div>
  );
}

const styles = {
  container: {
    textAlign: "center",
    margin: "50px auto",
    width: "80%",
  },
  title: {
    fontSize: "2rem",
    marginBottom: "20px",
  },
  searchContainer: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    gap: "10px",
    marginBottom: "30px",
    position: "relative",
  },
  input: {
    width: "600px",
    padding: "15px",
    fontSize: "1.2rem",
    borderRadius: "25px",
    border: "1px solid #ccc",
    background: "linear-gradient(to right, #f7f7f7, #e0e0e0)",
    outline: "none",
    boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
  },
  imageUploadContainer: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
  },
  icon: {
    cursor: "pointer",
    fontSize: "1.5rem",
  },
  previewContainer: {
    position: "relative",
    display: "inline-block",
  },
  imagePreview: {
    width: "100px",
    height: "100px",
    objectFit: "cover",
    borderRadius: "10px",
    border: "1px solid #ddd",
  },
  removeIcon: {
    position: "absolute",
    top: "5px",
    right: "5px",
    width: "20px",
    height: "20px",
    backgroundColor: "#ff4d4f",
    color: "#fff",
    borderRadius: "50%",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontSize: "0.8rem",
    cursor: "pointer",
    boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.2)",
  },
  buttonContainer: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    gap: "10px",
    marginTop: "20px",
  },
  button: {
    padding: "15px 40px",
    fontSize: "1.2rem",
    backgroundColor: "#007bff",
    color: "#fff",
    border: "none",
    borderRadius: "25px",
    cursor: "pointer",
    boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
    transition: "background-color 0.3s ease",
  },
  clearButton: {
    padding: "15px 40px",
    fontSize: "1.2rem",
    backgroundColor: "#d3d3d3",
    color: "#000",
    border: "none",
    borderRadius: "25px",
    cursor: "pointer",
    boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
    transition: "background-color 0.3s ease",
  },
  loading: {
    marginTop: "20px",
    fontSize: "1.5rem",
    color: "#007bff",
  },
  errorMessage: {
    marginTop: "20px",
    fontSize: "1.2rem",
    color: "red",
  },
  resultsContainer: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))",
    gap: "20px",
    marginTop: "20px",
  },
  resultItem: {
    textAlign: "center",
    position: "relative",
  },
  resultImage: {
    width: "200px",
    height: "200px",
    objectFit: "cover",
    marginBottom: "10px",
    backgroundColor: "#d3d3d3",
  },
  imageLoading: {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    color: "#007bff",
    fontSize: "1rem",
  },
};

export default App;
