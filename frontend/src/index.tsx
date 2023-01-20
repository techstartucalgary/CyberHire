import React from "react";
import ReactDOM from "react-dom/client";
import { Route, Routes, HashRouter } from "react-router-dom";
import "./styles/index.css";
import App from "./App";
import About from "./Pages/About";
import Privacy from "./Pages/Privacy";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <HashRouter>
    <Routes>
      <Route path="" element={<App />} />
      <Route path="/about" element={<About />} />
      <Route path="/privacy" element={<Privacy />}/>
    </Routes>
  </HashRouter>
);
