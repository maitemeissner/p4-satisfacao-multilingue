import os
import csv
import io
import psycopg2
import psycopg2.extras
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp.modelo import ModeloPreditor
from lgpd.anonymizer import Anonymizer

app = Flask(__name__)
CORS(app)

modelo = ModeloPreditor()
anonymizer = Anonymizer()

def get_db():
    return psycopg2.connect(
        host=os.environ.get('NEON_HOST'),
        dbname=os.environ.get('NEON_DATABASE', 'neondb'),
        user=os.environ.get('NEON_USER'),
        password=os.environ.get('NEON_PASSWORD'),
        sslmode='require'
    )

def init_db():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id SERIAL PRIMARY KEY,
                texto_anonimizado TEXT,
                score REAL,
                idioma VARCHAR(10),
                plataforma VARCHAR(50),
                data DATE DEFAULT CURRENT_DATE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB init warning: {e}")

init_db()

@app.route("/prever", methods=["POST"])
def prever():
    data = request.get_json()
    if not data or "texto" not in data:
        return jsonify({"erro": "Campo 'texto' é obrigatório"}), 400
    texto = data["texto"]
    score, classe, confianca = modelo.prever(texto)
    return jsonify({"score": score, "classe": classe, "confianca": confianca})

@app.route("/stats", methods=["GET"])
def stats():
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT COUNT(*) as total FROM reviews")
        total = cur.fetchone()["total"]
        cur.execute("SELECT idioma, AVG(score) as media FROM reviews GROUP BY idioma")
        por_idioma = {r["idioma"]: float(r["media"]) for r in cur.fetchall()}
        cur.execute("SELECT plataforma, AVG(score) as media FROM reviews GROUP BY plataforma")
        por_plataforma = {r["plataforma"]: float(r["media"]) for r in cur.fetchall()}
        cur.close()
        conn.close()
        return jsonify({
            "media_por_idioma": por_idioma,
            "media_por_plataforma": por_plataforma,
            "total_reviews": total
        })
    except Exception as e:
        return jsonify({"erro": str(e), "total_reviews": 0}), 500

@app.route("/upload-csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    file = request.files["file"]
    content = file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    count = 0
    conn = get_db()
    cur = conn.cursor()
    for row in reader:
        texto = row.get("texto", "")
        score = float(row.get("score", 3))
        idioma = row.get("idioma", "pt")
        plataforma = row.get("plataforma", "desconhecida")
        data = row.get("data", datetime.now().strftime("%Y-%m-%d"))
        texto_anonimizado = anonymizer.anonymize(texto)
        cur.execute(
            "INSERT INTO reviews (texto_anonimizado, score, idioma, plataforma, data) VALUES (%s, %s, %s, %s, %s)",
            (texto_anonimizado, score, idioma, plataforma, data)
        )
        count += 1
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"{count} reviews importadas com sucesso", "total": count})

@app.route("/relatorio-lgpd", methods=["GET"])
def relatorio_lgpd():
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM reviews ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"reviews": [dict(r) for r in rows]})
    except Exception as e:
        return jsonify({"erro": str(e), "reviews": []}), 500

if __name__ != "__main__":
    gunicorn_app = app
else:
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
