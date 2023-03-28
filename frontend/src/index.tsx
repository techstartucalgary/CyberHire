import React from "react";
import ReactDOM from "react-dom/client";
import { Route, Routes, HashRouter } from "react-router-dom";
import "./styles/index.css";
import App from "./App";
import About from "./Pages/About";
import Privacy from "./Pages/Privacy";
import SignUpPage from "./components/SignUp";
import LoginPage from "./components/SignIn";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);

root.render(
  <HashRouter>
    <Routes>
      <Route path="" element={<App />} />
      <Route path="/about" element={<About />} />
      <Route path="/privacy" element={<Privacy />}/>
	  <Route path="/signin" element={<LoginPage />} />
	  <Route path="/signup" element={<SignUpPage />} />
    </Routes>
  </HashRouter>
);
