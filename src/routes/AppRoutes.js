import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Tp from "../Tp";
import ManualTag from "../ManualTag";
import App from "../App";
import Home from "../Home";
import { Quiz } from "../Quiz";
// import Home from "../Home";

const AppRoutes = () => {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/quiz" element={<Quiz />} />
        <Route path="/ad" element={<App />} />
        <Route path="/tp" element={<Tp />} />
        <Route path="/manual_tag" element={<ManualTag />} />
      </Routes>
    </>
  );
};

export default AppRoutes;
