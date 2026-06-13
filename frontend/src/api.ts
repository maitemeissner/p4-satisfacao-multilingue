import axios from "axios"

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000"

const client = axios.create({ baseURL: BASE_URL })

const api = {
  async prever(texto: string) {
    const { data } = await client.post("/prever", { texto })
    return data
  },

  async getStats() {
    const { data } = await client.get("/stats")
    return data
  },

  async uploadCsv(file: File) {
    const form = new FormData()
    form.append("file", file)
    const { data } = await client.post("/upload-csv", form)
    return data
  },

  async getRelatorioLgpd() {
    const { data } = await client.get("/relatorio-lgpd")
    return data
  },
}

export default api
