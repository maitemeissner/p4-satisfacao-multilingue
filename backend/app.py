import os
import csv
import io
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp.modelo import ModeloPreditor
from lgpd.anonymizer import Anonymizer

app = Flask(__name__)
CORS(app)

modelo = ModeloPreditor()
anonymizer = Anonymizer()

reviews_db: list[dict] = []

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
    if not reviews_db:
        return jsonify({
            "media_por_idioma": {},
            "media_por_plataforma": {},
            "media_por_periodo": {},
            "total_reviews": 0
        })
    idiomas: dict[str, list[float]] = {}
    plataformas: dict[str, list[float]] = {}
    periodos: dict[str, list[float]] = {}
    for r in reviews_db:
        idiomas.setdefault(r["idioma"], []).append(r["score"])
        plataformas.setdefault(r["plataforma"], []).append(r["score"])
        if "data" in r and r["data"]:
            try:
                mes = datetime.strptime(r["data"], "%Y-%m-%d").strftime("%Y-%m")
                periodos.setdefault(mes, []).append(r["score"])
            except ValueError:
                pass
    return jsonify({
        "media_por_idioma": {k: sum(v) / len(v) for k, v in idiomas.items()},
        "media_por_plataforma": {k: sum(v) / len(v) for k, v in plataformas.items()},
        "media_por_periodo": {k: sum(v) / len(v) for k, v in periodos.items()},
        "total_reviews": len(reviews_db)
    })

@app.route("/upload-csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    file = request.files["file"]
    content = file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    count = 0
    for row in reader:
        texto = row.get("texto", "")
        score = float(row.get("score", 3))
        idioma = row.get("idioma", "pt")
        plataforma = row.get("plataforma", "desconhecida")
        data = row.get("data", datetime.now().strftime("%Y-%m-%d"))
        texto_anonimizado = anonymizer.anonymize(texto)
        reviews_db.append({
            "id": len(reviews_db) + 1,
            "texto_anonimizado": texto_anonimizado,
            "score": score,
            "idioma": idioma,
            "plataforma": plataforma,
            "data": data,
        })
        count += 1
    return jsonify({"message": f"{count} reviews importadas com sucesso", "total": count})

@app.route("/relatorio-lgpd", methods=["GET"])
def relatorio_lgpd():
    return jsonify({"reviews": reviews_db})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
