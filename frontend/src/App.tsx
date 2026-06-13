import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom"
import Dashboard from "./pages/Dashboard"
import Predizer from "./pages/Predizer"
import Reviews from "./pages/Reviews"

function App() {
  return (
    <BrowserRouter>
      <div style={{ fontFamily: "sans-serif", padding: "1rem" }}>
        <nav style={{ display: "flex", gap: "1rem", marginBottom: "1rem", borderBottom: "1px solid #ccc", paddingBottom: "0.5rem" }}>
          <NavLink to="/" end style={{ textDecoration: "none", fontWeight: "bold" }}>Dashboard</NavLink>
          <NavLink to="/predizer" style={{ textDecoration: "none", fontWeight: "bold" }}>Predizer</NavLink>
          <NavLink to="/reviews" style={{ textDecoration: "none", fontWeight: "bold" }}>Reviews</NavLink>
        </nav>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/predizer" element={<Predizer />} />
          <Route path="/reviews" element={<Reviews />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
