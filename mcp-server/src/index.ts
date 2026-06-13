import express from "express";
const app = express();
app.use(express.json());
const PORT = parseInt(process.env.PORT || "3001");
app.get("/health", (_r, res) => res.json({ status: "ok" }));
app.post("/mcp/analisar", (req, res) => {
  const { texto, idioma } = req.body;
  const score = Math.min(5, Math.max(1, Math.random() * 5));
  res.json({ score: score.toFixed(2), idioma, sentimento: score >= 4 ? "positivo" : score >= 3 ? "neutro" : "negativo" });
});
app.listen(PORT, () => console.log(`MCP Satisfacao running on ${PORT}`));