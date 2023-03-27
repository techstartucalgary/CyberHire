import React from "react";
import ReactDOM from "react-dom/client";
import { Route, Routes, HashRouter } from "react-router-dom";
import "./styles/index.css";
import App from "./pages/App";
import About from "./pages/About";
import Privacy from "./pages/Privacy";
import TopBar from "./components/TopBar";
import ApplicantHome from "./pages/ApplicantHome";
import NotFound from "./pages/NotFound";

const root = ReactDOM.createRoot(
  document.getElementById("root")
);
root.render(
  <HashRouter>
	<TopBar/>
    <Routes>
      <Route path="" element={<App />} />
      <Route path="/about" element={<About />} />
      <Route path="/privacy" element={<Privacy />}/>
      <Route path="/app" element={<ApplicantHome />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  </HashRouter>
);
