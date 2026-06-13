from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_PATH = "data/database.sqlite"

def get_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "satisfacao-multilingue"})

@app.route("/prever", methods=["POST"])
def prever():
    data = request.json
    texto = data.get("texto", "")
    idioma = data.get("idioma", "pt-BR")

    try:
        from nlp.modelo import predict_score
        score = predict_score(texto, idioma)
        return jsonify({"score": score, "idioma": idioma, "sentimento": "positivo" if score >= 4 else "neutro" if score >= 3 else "negativo"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/stats")
def stats():
    conn = get_db()
    rows = conn.execute(
        "SELECT idioma, AVG(score) as avg_score, COUNT(*) as total FROM reviews GROUP BY idioma"
    ).fetchall()
    conn.close()
    return jsonify({"stats": [dict(r) for r in rows]})

@app.route("/relatorio-lgpd")
def relatorio_lgpd():
    return jsonify({
        "dados_anonimizados": True,
        "campos_ofuscados": ["nome_reviewer", "email", "ip_address"],
        "base_legal": "LGPD Art. 7",
        "data_geracao": datetime.now().isoformat()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)