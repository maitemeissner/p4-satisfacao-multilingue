import { useEffect, useState } from "react"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts"
import api from "../api"

interface Stats {
  media_por_idioma: Record<string, number>
  media_por_plataforma: Record<string, number>
  media_por_periodo: Record<string, number>
  total_reviews: number
}

function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null)

  useEffect(() => {
    api.getStats().then(setStats).catch(console.error)
  }, [])

  if (!stats) return <p>Carregando estatísticas...</p>

  const idiomaData = Object.entries(stats.media_por_idioma).map(([k, v]) => ({ nome: k, media: v }))
  const plataformaData = Object.entries(stats.media_por_plataforma).map(([k, v]) => ({ nome: k, media: v }))
  const periodoData = Object.entries(stats.media_por_periodo).map(([k, v]) => ({ nome: k, media: v }))

  return (
    <div>
      <h1>Dashboard de Satisfação</h1>
      <p>Total de reviews analisadas: <strong>{stats.total_reviews}</strong></p>

      <h2>Média por Idioma</h2>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={idiomaData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="nome" />
          <YAxis domain={[0, 5]} />
          <Tooltip />
          <Legend />
          <Bar dataKey="media" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>

      <h2>Média por Plataforma</h2>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={plataformaData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="nome" />
          <YAxis domain={[0, 5]} />
          <Tooltip />
          <Legend />
          <Bar dataKey="media" fill="#82ca9d" />
        </BarChart>
      </ResponsiveContainer>

      <h2>Média por Período</h2>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={periodoData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="nome" />
          <YAxis domain={[0, 5]} />
          <Tooltip />
          <Legend />
          <Bar dataKey="media" fill="#ffc658" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default Dashboard
