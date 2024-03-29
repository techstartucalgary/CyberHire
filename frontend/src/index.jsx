import React from "react";
import ReactDOM from "react-dom/client";
import { Route, Routes, HashRouter } from "react-router-dom";
import "./styles/index.css";
import LandingPage from "./pages/LandingPage";
import About from "./pages/About";
import Privacy from "./pages/Privacy";
import TopBar from "./components/TopBar";
import ApplicantHome from "./pages/ApplicantHome";
import NotFound from "./pages/NotFound";
import RecruiterHome from "./pages/RecruiterHome";
import SignUpPage from "./components/SignUp";
import LoginPage from "./components/SignIn";
import CreateProfile from "./pages/createProfile";
import SkillsSelector from "./pages/skills";
import EditProfile from "./pages/editProfile";
import RecruiterApplicantsPage from "./pages/RecruiterApplicants";

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <HashRouter>
    <TopBar />
    <Routes>
      <Route path="" element={<LandingPage />} />
      <Route path="/signin" element={<LoginPage />} />
      <Route path="/signup" element={<SignUpPage />} />
      <Route path="/about" element={<About />} />
      <Route path="/privacy" element={<Privacy />} />
      <Route path="/app" element={<ApplicantHome />} />
      <Route path="/recruiterHome" element={<RecruiterHome />} />
      <Route path="/createProfile" element={<CreateProfile />} />
      <Route path="/editProfile" element={<EditProfile />} />
      <Route path="/skills" element={<SkillsSelector />} />
      <Route path="/recruiterApplicant" element={<RecruiterApplicantsPage />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  </HashRouter>,
);
