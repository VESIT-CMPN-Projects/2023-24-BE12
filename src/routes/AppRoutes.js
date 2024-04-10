import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Tp from "../Tp";
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
      </Routes>
    </>
  );
};

export default AppRoutes;
