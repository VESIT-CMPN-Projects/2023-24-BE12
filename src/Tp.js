import React, { useState } from "react";
import axios from "axios";

const Tp = () => {
  const [generatedImage, setGeneratedImage] = useState(null);
  const [maskImage, setMaskImage] = useState(null);
  const [showGeneratedImageUploadButton, setShowGeneratedImageUploadButton] = useState(true);
  const [showMaskUploadButton, setShowMaskUploadButton] = useState(true);
  const [processedImageUrl, setProcessedImageUrl] = useState(null);
  const [error, setError] = useState(null);

  const handleGeneratedImageUpload = (event) => {
    const file = event.target.files[0];
    setGeneratedImage(URL.createObjectURL(file));
    setShowGeneratedImageUploadButton(false);
  };

  const handleMaskUpload = (event) => {
    const file = event.target.files[0];
    setMaskImage(URL.createObjectURL(file));
    setShowMaskUploadButton(false);
  };

  const handleMergeClick = async () => {
    try {
      const generatedImageFile = await fetch(generatedImage).then(res => res.blob());
      const maskImageFile = await fetch(maskImage).then(res => res.blob());
  
      const formData = new FormData();
      formData.append('generatedImage', generatedImageFile, 'generatedImage.png');
      formData.append('maskImage', maskImageFile, 'maskImage.png');
  
      const response = await axios.post('http://localhost:5000/run_merge', formData);
      const { image_with_text } = response.data;
  
      // Create a Blob from the base64-encoded image data
      const blob = await fetch(`data:image/jpeg;base64,${image_with_text}`).then(res => res.blob());
  
      // Create a URL for the Blob object
      const imageUrl = URL.createObjectURL(blob);
      setProcessedImageUrl(imageUrl);
      setError(null); // Reset error state
    } catch (error) {
      console.error('Error merging images:', error);
      setError('Error merging images. Please try again.');
    }
  };

  return (
    <div className="appp">
      <header>
        <img src="./AdGenAi.png" alt="Your Website Logo" />
        <span className="tagline">Make magic with AI-powered tools.</span>
      </header>
      <div style={{ margin: "20px 480px", alignItems: "center", justifyContent: "center" }}>
        <>
          {!processedImageUrl && (
            <>
              <div className="button-container">
                <div className="dotted-box" style={{ width: generatedImage ? "512px" : "512px", height: generatedImage ? "512px" : "256px" }}>
                  {generatedImage && <img src={generatedImage} alt="Generated Image" />}
                  {showGeneratedImageUploadButton && (
                    <>
                      <input type="file" id="uploadGeneratedImage" onChange={handleGeneratedImageUpload} />
                      <label htmlFor="uploadGeneratedImage">Upload Generated Image</label>
                    </>
                  )}
                </div>
              </div>
              <div className="button-container">
                <div className="dotted-box" style={{ width: maskImage ? "512px" : "512px", height: maskImage ? "512px" : "256px" }}>
                  {maskImage && <img src={maskImage} alt="Mask Image" />}
                  {showMaskUploadButton && (
                    <>
                      <input type="file" id="uploadMask" onChange={handleMaskUpload} />
                      <label htmlFor="uploadMask">Upload Mask</label>
                    </>
                  )}
                </div>
              </div>
              {!showMaskUploadButton && (
                <div className="button-container">
                  <button onClick={handleMergeClick}>Merge</button>
                </div>
              )}
            </>
          )}
          {processedImageUrl && (
            <div className="button-container2">
              <div className="dotted-box2">
                <img src={processedImageUrl} alt="Processed Image" />
                <p>Processed Image</p>
              </div>
            </div>
          )}
          {error && <p className="error-message">{error}</p>}
        </>
      </div>
      <div style={{ height: "5vh" }}></div>
    </div>
  );
};

export default Tp;
