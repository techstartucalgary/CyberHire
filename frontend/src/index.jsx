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
import SignUpPage from "./components/SignUp";
import LoginPage from "./components/SignIn";
import CreateProfile from "./pages/createProfile";
import SkillsSelector from "./pages/skills";
import EditProfile from "./pages/editProfile";


const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <HashRouter>
    <TopBar />
    <Routes>
      <Route path="" element={<App />} />
      <Route path="/about" element={<About />} />
      <Route path="/privacy" element={<Privacy />} />
      <Route path="/app" element={<ApplicantHome />} />
      <Route path="/signin" element={<LoginPage />} />
      <Route path="/signup" element={<SignUpPage />} />
      <Route path="/createProfile" element={<CreateProfile />} />
      <Route path="/skills" element={<SkillsSelector />} />
      <Route path="/editProfile" element={<EditProfile />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  </HashRouter>
);
