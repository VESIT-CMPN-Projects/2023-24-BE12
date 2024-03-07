import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Tp from "../Tp";
import App from "../App";

const AppRoutes = () => {
  return (
    <>
      <Routes>
        <Route path="/tp" element={<Tp />} />
        <Route path="*" element={<App />} />
      </Routes>
    </>
  );
};

export default AppRoutes;
