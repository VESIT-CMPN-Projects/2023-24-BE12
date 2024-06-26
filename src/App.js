import React, { useState } from "react";
import "./App.css";
import axios from "axios";
import "./home.css";

import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

const YourComponent = () => {
  // const [productDescription, setProductDescription] = useState("");
  const [generatedImages, setGeneratedImages] = useState([]);
  const [selectedImageIndex, setSelectedImageIndex] = useState(null);
  const [selectedTaglines, setSelectedTaglines] = useState([]);
  const [selectedTaglineIndex, setSelectedTaglineIndex] = useState(null); // Track selected tagline index
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showTaglines, setShowTaglines] = useState(false); // Added state variable
  const [showHeading, setShowHeading] = useState(false); // State for heading visibility
  // const[]
  const [selectedImage, setSelectedImage] = useState([]);
  const [selectedTagline, setSelectedTagline] = useState(null);
  const [imageArray, setImageArray] = useState([]);
  const [tpVisibility, setTpVisibility] = useState(false);
  const [selectedProductType, setProductSelectedType] = useState("");

  const [productDescription, setProductDescription] = useState(() => {
    const userAnswersString = localStorage.getItem("userAnswers");
    console.log(userAnswersString);
    if (userAnswersString) {
      const parsedAnswers = JSON.parse(userAnswersString);
      // Remove the last answer from parsedAnswers
      parsedAnswers.pop();
      return parsedAnswers; // Return parsed answers if found
    } else {
      return []; // Return empty array if not found
    }
  });


  const selectedImages = (src) => {
    setTpVisibility(true);
    console.log("img selected");
    localStorage.setItem("storedImages", src);
    setImageArray([...imageArray, src]);
    console.log(imageArray);
  };
  const handleGenerateAd = () => {
    setLoading(true);
    sendProductDescriptionToGenImage(productDescription);
    sendProductDescriptionToFlaskTagline(productDescription);
  };

  const sendProductDescriptionToFlaskTagline = (productDescription) => {
    const flaskURL = "http://localhost:5000/run_script_tagline";
  
    axios
      .post(flaskURL, { data: productDescription })
      .then((response) => {
        console.log(response.data);
        if (response.data) {
          // Remove numbering and split taglines, then trim extra whitespace
          const taglinesArray = response.data.split("\n")
            .map(tagline => tagline.replace(/^\d+\.\s*/, '').trim())
            .filter(tagline => tagline !== ''); // Filter out empty strings
          setSelectedTaglines(taglinesArray);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        setError("Failed to generate tagline. Please try again.");
      })
      .finally(() => setLoading(false));
  };
  
  

  const sendProductDescriptionToFlaskPrompt = (productDescription) => {
    const flaskURL = "http://localhost:5000/run_script_prompt_maker";

    axios
      .post(flaskURL, { data: productDescription })
      .then((response) => {
        console.log(response.data);
        if (response.data) {
          setProductDescription([response.data]);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const sendProductDescriptionToGenImage = (productDescription) => {
    const flaskURL = "http://localhost:5000/run_script_image";

    axios
      .post(flaskURL, { data: productDescription })
      .then((response) => {
        if (response.data && response.data.images) {
          const images = response.data.images.map((imageData) => {
            const img = new Image();
            img.src = `data:image/png;base64,${imageData}`;
            return img;
          });
          setGeneratedImages(images);
        } else {
          console.error("Invalid response from Flask:", response.data);
          setError("Failed to generate image. Please try again.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        setError("Failed to generate image. Please try again.");
      })
      .finally(() => setLoading(false));
  };

  const handleRandomQuery = () => {
    setLoading(true);
    sendProductDescriptionToFlaskPrompt(productDescription);
  };

  // Handle selecting tagline
  const handleSelectTagline = (index) => {
    setSelectedTaglineIndex(index);
    setSelectedTagline(selectedTaglines[index]);
  };

  // Handle selecting image
  const handleSelectImage = (index) => {
    setSelectedImageIndex(index);
    setSelectedImage(generatedImages[index]);
  };

  const handleTaglineCheckboxChange = (index, tagline) => {
    if (selectedTaglineIndex === index) {
      setSelectedTaglineIndex(null);
      setSelectedTagline(null);
    } else {
      localStorage.setItem("tagline", tagline);
      setSelectedTaglineIndex(index);
      setSelectedTagline(selectedTaglines[index]);
    }
  };

  const handleImageCheckboxChange = (img, index) => {
    if (selectedImageIndex === index) {
      setSelectedImageIndex(null);
      setSelectedImage(null);
    } else {
      setSelectedImageIndex(img.src);
      setSelectedImage(generatedImages[index]);
    }
  };

  const lastAnswer = localStorage.getItem("lastAnswer");
  console.log(lastAnswer);
  
  // Define mergeLink outside of if-else blocks
  let mergeLink;
  if (lastAnswer === "Yes") {
    mergeLink = "/tp";
  } else {
    mergeLink = "/manual_tag";
  }


  return (
    <div>
      <header>
        {/* <img src="./AdGenAi.png" alt="Your Website Logo" /> */}
        <span className="logo">ADGENAI</span>
        {/* <span className="tagline">Make magic with AI-powered tools.</span> */}
      </header>

      <div class="appp">
        <section>
          {/* Search bar centered with text "Enter your product description" */}
          <input
            className="search-bar"
            type="text"
            placeholder="Enter your product description"
            value={productDescription}
            onChange={(e) => setProductDescription(e.target.value)}
            // style={{ textAlign: "center", width: "80%", margin: "20px auto" }}
          />
        </section>

        {/* Buttons "Convert To Image Caption" and "Generate AD" side-by-side */}
        <section className="button-section">
          <button className="button-sec" onClick={handleRandomQuery}>
            Convert To Image Caption
          </button>
          {/* Add spacing between buttons */}
          {/* <span style={{ margin: "0 10px" }} /> */}
          <button
            className="button-sec"
            onClick={() => {
              handleGenerateAd();
              setShowTaglines(true);
              setShowHeading(true);
            }}
          >
            Generate AD
          </button>
        </section>

        <section>
          <div>
            {showHeading && (
              <h2 className="typewriter-animation">
                Here are the generated taglines for the product
              </h2>
            )}

            {selectedTaglines.map((tagline, index) => (
              <p key={index} className="caption-class">
                {/* // className={index === selectedTaglineIndex ? "selected" : ""} */}
                {/* // onClick={() => handleSelectTagline(index)} */}

                <input
                  width={"5%"}
                  type="radio"
                  checked={selectedTaglineIndex === index}
                  onChange={() => handleTaglineCheckboxChange(index, tagline)}
                />
                <span
                  className="typewriter-animation"
                  style={{ marginLeft: "5px" }}
                >
                  {tagline}
                </span>
              </p>
            ))}
            {error && <p className="error-message">{error}</p>}
            {loading && <p>Loading...</p>}
          </div>
          <div className="image-grid container">
            {generatedImages.map((img, index) => (
              <div key={index}>
                <input
                  type="radio"
                  checked={selectedImageIndex === index}
                  onChange={() => selectedImages(img.src)}
                />
                <figure className="card">
                  {/* {setImgSrcSource(img)} */}
                  <img src={img.src} alt={`Generated ${index}`} />
                  <figcaption>Image {index + 1}</figcaption>
                </figure>
              </div>
            ))}
          </div>
        </section>
        <section className="button-section">
          <Link to={mergeLink}>
            <button className="button-sec">Merge Image and Caption</button>
          </Link>
        </section>
        <div style={{ height: "40vh" }}></div>
      </div>

      {/* <Tp visible={tpVisibility} images={imageArray} /> */}
    </div>
  );
};

export default YourComponent;
