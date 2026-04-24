import React from "react";
import ReactDOM from "react-dom/client";
import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";
import "./index.css";
import LoginPage from "./pages/LoginPage";
import ContestPage from "./pages/ContestPage";
import ContestDetailsPage from "./pages/ContestDetailsPage";
import ProblemSolvePage from "./pages/ProblemSolvePage";

ReactDOM.createRoot(
  document.getElementById("root")!
).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<ContestPage />} />
      <Route path="/login" element={<LoginPage />} />
    </Routes>
  </BrowserRouter>
);