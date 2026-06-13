import { useState, useEffect } from 'react';

function App() {
  const [texto, setTexto] = useState('');
  const [idioma, setIdioma] = useState('pt-BR');
  const [resultado, setResultado] = useState<any>(null);
  const [stats, setStats] = useState<any[]>([]);

  useEffect(() => {
    fetch('/api/stats').then(r => r.json()).then(d => setStats(d.stats || [])).catch(() => {});
  }, []);

  const prever = async () => {
    const res = await fetch('/api/prever', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ texto, idioma }),
    });
    setResultado(await res.json());
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: 600, margin: '0 auto' }}>
      <h1>Preditor de Satisfação Multilíngue</h1>
      <textarea value={texto} onChange={e => setTexto(e.target.value)} rows={4} style={{ width: '100%' }} placeholder="Digite um review..." />
      <select value={idioma} onChange={e => setIdioma(e.target.value)} style={{ marginTop: '0.5rem' }}>
        <option value="pt-BR">Português</option>
        <option value="en-US">English</option>
        <option value="es-ES">Español</option>
      </select>
      <button onClick={prever} style={{ marginLeft: '0.5rem' }}>Analisar</button>

      {resultado && (
        <div style={{ marginTop: '1rem', padding: '1rem', background: '#e9ecef' }}>
          <p>Score: <strong>{resultado.score}</strong>/5</p>
          <p>Sentimento: <strong>{resultado.sentimento}</strong></p>
        </div>
      )}

      <h2 style={{ marginTop: '2rem' }}>Estatísticas</h2>
      <ul>
        {stats.map((s: any, i: number) => (
          <li key={i}>{s.idioma}: média {s.avg_score?.toFixed(2)} ({s.total} reviews)</li>
        ))}
      </ul>
    </div>
  );
}
export default App;