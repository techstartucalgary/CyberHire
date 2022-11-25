import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router } from "react-router-dom";
import { Route, Routes } from "react-router-dom";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <Router>
    <Routes>
      {/* TODO: Figure out why exact doesn't work */}
      <Route path="" element={<App />} />
      <Route path="/about" element={<App />} />
    </Routes>
  </Router>
);

reportWebVitals();
