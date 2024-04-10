import React from "react";
import "./App.css";
import { json } from "react-router-dom";

const Tp = () => {
  const images = [];
  let imageString = JSON.stringify(localStorage.getItem("storedImages"));
  let final = imageString.substring(1, imageString.length - 1);

  let tagline = localStorage.getItem("tagline");
  let finalTagLine = tagline.substring(1, tagline.length - 1);
  console.log(final);
  // let second=imageString.sub
  // console.log(imageString);
  // imageString=
  // let sp = imageString.split("src:");
  // console.log(sp);
  // const images = [""];
  // console.log("tp me aaya");
  // return images.map((src) => {
  //   return (
  //     <div>
  //       {console.log(src)}
  //       <img src={src} alt="" />
  //     </div>
  //   );
  // });
  return (
    <div className="appp">
      <header>
        <img src="./AdGenAi.png" alt="Your Website Logo" />
        <span className="tagline">Make magic with AI-powered tools.</span>
      </header>
      <div
        style={{
          margin: "20px 480px",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <>
          <img src={final} alt="jh" />
          <p>{finalTagLine}</p>
        </>
      </div>
      <div style={{ height: "5vh" }}></div>
    </div>
  );
};

export default Tp;
