import React, { useState } from "react";
import "./App.css";
import axios from "axios";

const YourComponent = () => {
  const [productDescription, setProductDescription] = useState("");
  const [generatedImage, setGeneratedImage] = useState(null);
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
    // Define the Flask API URL
    const flaskURL = 'http://localhost:5000/run_script_prompt_maker';
  
    // Make a POST request to your Flask API
    axios.post(flaskURL, { data: productDescription })
      .then(response => {
        // Handle the response from Flask
        console.log(response.data);
  
        // Set the response as the taglines
        if (response.data) {
          setProductDescription([response.data]);
        }
      })
      .catch(error => {
        // Handle errors (e.g., display an error message)
        console.error('Error:', error);
      });
  };

  const sendProductDescriptionToGenImage = (productDescription) => {
    const flaskURL = 'http://localhost:5000/run_script_image';

    axios.post(flaskURL, { data: productDescription })
      .then(response => {
        if (response.data && response.data.image) {
          const img = new Image();
          img.src = `data:image/png;base64,${response.data.image}`;
          setGeneratedImage(img);
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

  const handleRandomQuery = () => {
    setLoading(true);
    sendProductDescriptionToFlaskPrompt(productDescription);
  };

  return (
    <div>
      {/* Header Section */}
      {/* ... (unchanged) */}

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

      {/* Generated Image Section */}
      <section>
        {generatedImage && (
          <div>
            <h2 className="animated-heading">
              Here is the generated image for the product
            </h2>
            <img src={generatedImage.src} alt="Generated Product" />
          </div>
        )}
        {error && <p className="error-message">{error}</p>}
        {loading && <p>Loading...</p>}
      </section>

      {/* Random Query and Generate AD Section */}
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
