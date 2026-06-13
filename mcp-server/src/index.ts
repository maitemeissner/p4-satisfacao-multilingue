import express from "express"
import axios from "axios"

const app = express()
const PORT = process.env.PORT || 3001
const FLASK_URL = process.env.FLASK_URL || "http://localhost:5000"

app.use(express.json())

app.get("/health", (_req, res) => {
  res.json({ status: "ok", server: "p4-mcp-server" })
})

app.get("/api/predictions", async (_req, res) => {
  try {
    const resp = await axios.get(`${FLASK_URL}/stats`)
    res.json(resp.data)
  } catch {
    res.status(502).json({ erro: "Falha ao conectar com backend Flask" })
  }
})

app.post("/api/predict", async (req, res) => {
  try {
    const { texto } = req.body
    if (!texto) {
      return res.status(400).json({ erro: "Campo 'texto' é obrigatório" })
    }
    const resp = await axios.post(`${FLASK_URL}/prever`, { texto })
    res.json(resp.data)
  } catch {
    res.status(502).json({ erro: "Falha ao conectar com backend Flask" })
  }
})

app.get("/api/stats", async (_req, res) => {
  try {
    const resp = await axios.get(`${FLASK_URL}/relatorio-lgpd`)
    res.json(resp.data)
  } catch {
    res.status(502).json({ erro: "Falha ao conectar com backend Flask" })
  }
})

app.listen(PORT, () => {
  console.log(`MCP Server rodando na porta ${PORT}`)
})
