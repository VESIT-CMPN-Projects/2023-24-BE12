import React, { useState } from "react";
import "./App.css";
import axios from "axios";

const YourComponent = () => {
  const [productDescription, setProductDescription] = useState("");
  const [generatedImages, setGeneratedImages] = useState([]);
  const [selectedImageIndex, setSelectedImageIndex] = useState(null);
  const [selectedTaglines, setSelectedTaglines] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerateAd = () => {
    setLoading(true);
    sendProductDescriptionToGenImage(productDescription);
    sendProductDescriptionToFlaskTagline(productDescription);
  };

  const sendProductDescriptionToFlaskTagline = (productDescription) => {
    const flaskURL = 'http://localhost:5000/run_script_tagline';

    axios.post(flaskURL, { data: productDescription })
      .then(response => {
        console.log(response.data);
        if (response.data) {
          setSelectedTaglines([response.data]);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        setError('Failed to generate tagline. Please try again.');
      })
      .finally(() => setLoading(false));
  };

  const sendProductDescriptionToFlaskPrompt = (productDescription) => {
    const flaskURL = 'http://localhost:5000/run_script_prompt_maker';
  
    axios.post(flaskURL, { data: productDescription })
      .then(response => {
        console.log(response.data);
        if (response.data) {
          setProductDescription([response.data]);
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  const sendProductDescriptionToGenImage = (productDescription) => {
    const flaskURL = 'http://localhost:5000/run_script_image';

    axios.post(flaskURL, { data: productDescription })
      .then(response => {
        if (response.data && response.data.images) {
          const images = response.data.images.map(imageData => {
            const img = new Image();
            img.src = `data:image/png;base64,${imageData}`;
            return img;
          });
          setGeneratedImages(images);
        } else {
          console.error('Invalid response from Flask:', response.data);
          setError('Failed to generate image. Please try again.');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        setError('Failed to generate image. Please try again.');
      })
      .finally(() => setLoading(false));
  };

  const handleImageClick = (index) => {
    setSelectedImageIndex(index);
  };

  const handleRandomQuery = () => {
    setLoading(true);
    sendProductDescriptionToFlaskPrompt(productDescription);
  };

  return (
    <div>
      <section>
        <h2>Here are the generated taglines for the product</h2>
        <div>
          {selectedTaglines.map((tagline, index) => (
            <p key={index}>
              <span className="typewriter-animation">{tagline}</span>
            </p>
          ))}
        </div>
        {error && <p className="error-message">{error}</p>}
        {loading && <p>Loading...</p>}
      </section>

      <section id="parentSection">
        <h2 className="animated-heading">
          Here are the generated images for the product
        </h2>
        <div className="image-grid">
          {generatedImages.map((img, index) => (
            <div
              key={index}
              className={`image-container ${selectedImageIndex !== null && selectedImageIndex !== index ? 'hidden' : ''}`}
              onClick={() => handleImageClick(index)}
            >
              <img src={img.src} alt={`Generated ${index}`} />
            </div>
          ))}
        </div>
      </section>

      <section>
        <button onClick={handleRandomQuery}>Convert To Image Caption</button>
        <input
          type="text"
          placeholder="Enter your product description"
          value={productDescription}
          onChange={(e) => setProductDescription(e.target.value)}
        />
        <button onClick={handleGenerateAd}>Generate AD</button>
      </section>
    </div>
  );
};

export default YourComponent;
