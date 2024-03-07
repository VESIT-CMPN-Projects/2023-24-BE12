// Import necessary components and routing library
import React from "react";
import { useLocation } from "react-router-dom"; // Replace with your routing library hook

const MergedContent = () => {
  const location = useLocation();
  const { imageURL, taglineText } = location.state;

  // Render the merged content using image and tagline data
  return (
    <div>
      <img src={imageURL} alt="Generated Image" />
      <p>{taglineText}</p>
    </div>
  );
};

export default MergedContent;
