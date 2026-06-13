import { useEffect, useState } from "react"
import api from "../api"

interface Review {
  id: number
  texto_anonimizado: string
  score: number
  idioma: string
  plataforma: string
  data: string
}

function Reviews() {
  const [reviews, setReviews] = useState<Review[]>([])

  useEffect(() => {
    api.getRelatorioLgpd().then((data) => setReviews(data.reviews || [])).catch(console.error)
  }, [])

  return (
    <div>
      <h1>Reviews Anonimizadas (LGPD)</h1>
      <p>Lista de avaliações com dados pessoais removidos conforme a Lei Geral de Proteção de Dados.</p>
      {reviews.length === 0 ? (
        <p>Nenhuma review disponível.</p>
      ) : (
        <table border={1} cellPadding={8} style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Texto Anonimizado</th>
              <th>Score</th>
              <th>Idioma</th>
              <th>Plataforma</th>
              <th>Data</th>
            </tr>
          </thead>
          <tbody>
            {reviews.map((r) => (
              <tr key={r.id}>
                <td>{r.id}</td>
                <td>{r.texto_anonimizado}</td>
                <td>{r.score}</td>
                <td>{r.idioma}</td>
                <td>{r.plataforma}</td>
                <td>{r.data}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default Reviews
