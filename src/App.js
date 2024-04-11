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
          setSelectedTaglines([response.data]);
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

  return (
    <div>
      <header>
        {/* <img src="./AdGenAi.png" alt="Your Website Logo" /> */}
        <span className="logo">ADGENAI</span>
        {/* <span className="tagline">Make magic with AI-powered tools.</span> */}
      </header>
      {/* <header className="home-header">
        <header
          data-thq="thq-navbar"
          className="navbarContainer home-navbar-interactive"
        >
          <span className="logo">ADGENAI</span>
          <div data-thq="thq-navbar-nav" className="home-desktop-menu">
            <div className="home-buttons"></div>
          </div>
          <div data-thq="thq-burger-menu" className="home-burger-menu">
            <svg viewBox="0 0 1024 1024" className="home-icon socialIcons">
              <path d="M128 554.667h768c23.552 0 42.667-19.115 42.667-42.667s-19.115-42.667-42.667-42.667h-768c-23.552 0-42.667 19.115-42.667 42.667s19.115 42.667 42.667 42.667zM128 298.667h768c23.552 0 42.667-19.115 42.667-42.667s-19.115-42.667-42.667-42.667h-768c-23.552 0-42.667 19.115-42.667 42.667s19.115 42.667 42.667 42.667zM128 810.667h768c23.552 0 42.667-19.115 42.667-42.667s-19.115-42.667-42.667-42.667h-768c-23.552 0-42.667 19.115-42.667 42.667s19.115 42.667 42.667 42.667z"></path>
            </svg>
          </div>
          <div
            data-thq="thq-mobile-menu"
            className="home-mobile-menu1 mobileMenu"
          >
            <div className="home-nav">
              <div className="home-top">
                <span className="logo">ADGENAI</span>
                <div data-thq="thq-close-menu" className="home-close-menu">
                  <svg
                    viewBox="0 0 1024 1024"
                    className="home-icon02 socialIcons"
                  >
                    <path d="M810 274l-238 238 238 238-60 60-238-238-238 238-60-60 238-238-238-238 60-60 238 238 238-238z"></path>
                  </svg>
                </div>
              </div>
              <nav className="home-links">
                <span className="home-nav12 bodySmall">Home</span>
                <span className="home-nav22 bodySmall">About</span>
                <span className="home-nav32 bodySmall">Services</span>
                <span className="home-nav42 bodySmall">Contact</span>
              </nav>
              <div className="home-buttons1">
                <button className="buttonFlat">Login</button>
                <button className="buttonFilled">Register</button>
              </div>
            </div>
            <div>
              <svg
                viewBox="0 0 950.8571428571428 1024"
                className="home-icon04 socialIcons"
              >
                <path d="M925.714 233.143c-25.143 36.571-56.571 69.143-92.571 95.429 0.571 8 0.571 16 0.571 24 0 244-185.714 525.143-525.143 525.143-104.571 0-201.714-30.286-283.429-82.857 14.857 1.714 29.143 2.286 44.571 2.286 86.286 0 165.714-29.143 229.143-78.857-81.143-1.714-149.143-54.857-172.571-128 11.429 1.714 22.857 2.857 34.857 2.857 16.571 0 33.143-2.286 48.571-6.286-84.571-17.143-148-91.429-148-181.143v-2.286c24.571 13.714 53.143 22.286 83.429 23.429-49.714-33.143-82.286-89.714-82.286-153.714 0-34.286 9.143-65.714 25.143-93.143 90.857 112 227.429 185.143 380.571 193.143-2.857-13.714-4.571-28-4.571-42.286 0-101.714 82.286-184.571 184.571-184.571 53.143 0 101.143 22.286 134.857 58.286 41.714-8 81.714-23.429 117.143-44.571-13.714 42.857-42.857 78.857-81.143 101.714 37.143-4 73.143-14.286 106.286-28.571z"></path>
              </svg>
              <svg
                viewBox="0 0 877.7142857142857 1024"
                className="home-icon06 socialIcons"
              >
                <path d="M585.143 512c0-80.571-65.714-146.286-146.286-146.286s-146.286 65.714-146.286 146.286 65.714 146.286 146.286 146.286 146.286-65.714 146.286-146.286zM664 512c0 124.571-100.571 225.143-225.143 225.143s-225.143-100.571-225.143-225.143 100.571-225.143 225.143-225.143 225.143 100.571 225.143 225.143zM725.714 277.714c0 29.143-23.429 52.571-52.571 52.571s-52.571-23.429-52.571-52.571 23.429-52.571 52.571-52.571 52.571 23.429 52.571 52.571zM438.857 152c-64 0-201.143-5.143-258.857 17.714-20 8-34.857 17.714-50.286 33.143s-25.143 30.286-33.143 50.286c-22.857 57.714-17.714 194.857-17.714 258.857s-5.143 201.143 17.714 258.857c8 20 17.714 34.857 33.143 50.286s30.286 25.143 50.286 33.143c57.714 22.857 194.857 17.714 258.857 17.714s201.143 5.143 258.857-17.714c20-8 34.857-17.714 50.286-33.143s25.143-30.286 33.143-50.286c22.857-57.714 17.714-194.857 17.714-258.857s5.143-201.143-17.714-258.857c-8-20-17.714-34.857-33.143-50.286s-30.286-25.143-50.286-33.143c-57.714-22.857-194.857-17.714-258.857-17.714zM877.714 512c0 60.571 0.571 120.571-2.857 181.143-3.429 70.286-19.429 132.571-70.857 184s-113.714 67.429-184 70.857c-60.571 3.429-120.571 2.857-181.143 2.857s-120.571 0.571-181.143-2.857c-70.286-3.429-132.571-19.429-184-70.857s-67.429-113.714-70.857-184c-3.429-60.571-2.857-120.571-2.857-181.143s-0.571-120.571 2.857-181.143c3.429-70.286 19.429-132.571 70.857-184s113.714-67.429 184-70.857c60.571-3.429 120.571-2.857 181.143-2.857s120.571-0.571 181.143 2.857c70.286 3.429 132.571 19.429 184 70.857s67.429 113.714 70.857 184c3.429 60.571 2.857 120.571 2.857 181.143z"></path>
              </svg>
              <svg
                viewBox="0 0 602.2582857142856 1024"
                className="home-icon08 socialIcons"
              >
                <path d="M548 6.857v150.857h-89.714c-70.286 0-83.429 33.714-83.429 82.286v108h167.429l-22.286 169.143h-145.143v433.714h-174.857v-433.714h-145.714v-169.143h145.714v-124.571c0-144.571 88.571-223.429 217.714-223.429 61.714 0 114.857 4.571 130.286 6.857z"></path>
              </svg>
            </div>
          </div>
        </header>
      </header> */}

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
          {/* <Link to="/tp"> */}.
          <a href="tp">
            <button className="button-sec">Merge Image and Caption</button>
          </a>
          {/* <a href="tp">
            <button className="button-sec">Automatic</button>
          </a> */}
          {/* </Link> */}
        </section>
        <div style={{ height: "40vh" }}></div>
      </div>

      {/* <Tp visible={tpVisibility} images={imageArray} /> */}
    </div>
  );
};

export default YourComponent;
