import { useState } from "react"
import api from "../api"

function Predizer() {
  const [texto, setTexto] = useState("")
  const [resultado, setResultado] = useState<{ score: number; classe: string; confianca: number } | null>(null)
  const [erro, setErro] = useState("")

  const handlePredizer = async () => {
    if (!texto.trim()) return
    try {
      setErro("")
      const res = await api.prever(texto)
      setResultado(res)
    } catch {
      setErro("Erro ao processar a previsão")
    }
  }

  return (
    <div>
      <h1>Preditor de Satisfação Multilíngue</h1>
      <p>Digite uma avaliação em Português, Inglês ou Espanhol para obter a previsão de satisfação.</p>
      <textarea
        rows={6}
        cols={80}
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
        placeholder="Ex: Ótimo produto, recomendo!"
        style={{ fontSize: "1rem", padding: "0.5rem", width: "100%", maxWidth: "600px" }}
      />
      <br />
      <button onClick={handlePredizer} style={{ marginTop: "0.5rem", padding: "0.5rem 1.5rem", fontSize: "1rem" }}>
        Predizer Satisfação
      </button>

      {erro && <p style={{ color: "red" }}>{erro}</p>}

      {resultado && (
        <div style={{ marginTop: "1rem", border: "1px solid #ccc", padding: "1rem", maxWidth: "400px" }}>
          <p><strong>Score:</strong> {resultado.score.toFixed(2)} / 5</p>
          <p><strong>Classificação:</strong> {resultado.classe}</p>
          <p><strong>Confiança:</strong> {(resultado.confianca * 100).toFixed(1)}%</p>
        </div>
      )}
    </div>
  )
}

export default Predizer
