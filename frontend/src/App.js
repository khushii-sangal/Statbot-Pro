import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [chart, setChart] = useState(null);
  const [loading, setLoading] = useState(false);

  const BASE_URL = "http://127.0.0.1:8000";

  // 📂 Select file
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // 🚀 Upload CSV
  const handleUpload = async () => {
    if (!file) {
      alert("Please select a CSV file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const res = await axios.post(`${BASE_URL}/upload/`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      alert(res.data.message);
    } catch (error) {
      console.error(error);
      alert("❌ Upload failed");
    } finally {
      setLoading(false);
    }
  };

  // 🤖 Ask question
  const handleAsk = async () => {
    if (!query) {
      alert("Please enter a question!");
      return;
    }

    try {
      setLoading(true);
      setChart(null);

      const res = await axios.post(`${BASE_URL}/ask/`, {
        query: query,
      });

      console.log("Response:", res.data);

      // ✅ HANDLE GRAPH RESPONSE
      if (res.data.response && res.data.response.graph) {
        setChart(`${BASE_URL}/static/chart.png`);
        setResponse("📊 Chart generated below");
      } else {
        setResponse(res.data.response);
      }

    } catch (error) {
      console.error(error);
      alert("❌ Error getting response");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1>📊 CSV AI Agent</h1>

      {/* Upload Section */}
      <div style={styles.card}>
        <h3>Upload CSV</h3>
        <input type="file" onChange={handleFileChange} />
        <br />
        <button onClick={handleUpload} style={styles.button}>
          Upload
        </button>
      </div>

      {/* Query Section */}
      <div style={styles.card}>
        <h3>Ask Question</h3>
        <input
          type="text"
          placeholder="e.g. What is total revenue?"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={styles.input}
        />
        <br />
        <button onClick={handleAsk} style={styles.button}>
          Ask
        </button>
      </div>

      {/* Loading */}
      {loading && <p>⏳ Processing...</p>}

      {/* Response */}
      {response && (
        <div style={styles.response}>
          <h3>Response:</h3>
          <p>{response}</p>
        </div>
      )}

      {/* Chart Display */}
      {chart && (
        <div style={{ marginTop: "20px" }}>
          <h3>Generated Chart:</h3>
          <img
            src={chart}
            alt="Chart"
            style={{ width: "500px", borderRadius: "10px" }}
          />
        </div>
      )}
    </div>
  );
}

// 🎨 Styling
const styles = {
  container: {
    textAlign: "center",
    padding: "30px",
    fontFamily: "Arial",
  },
  card: {
    margin: "20px auto",
    padding: "20px",
    border: "1px solid #ccc",
    borderRadius: "10px",
    width: "320px",
  },
  button: {
    marginTop: "10px",
    padding: "10px 15px",
    cursor: "pointer",
    borderRadius: "5px",
  },
  input: {
    width: "90%",
    padding: "8px",
    marginTop: "10px",
  },
  response: {
    marginTop: "20px",
    padding: "15px",
    border: "1px solid #aaa",
    borderRadius: "10px",
  },
};

export default App;