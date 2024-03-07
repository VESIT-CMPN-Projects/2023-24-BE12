const handleImageClick = (index) => {
  setSelectedImageIndex(index);
};

const handleTaglineClick = (index) => {
  setSelectedTagline(index); // update selected tagline state
};

 // const handleMergeClick = () => {
  //   const navigate = useNavigate();
  //   if (selectedImage !== null && selectedTagline !== null) {
  //     // Get selected image and tagline data
  //     const selectedImageURL = generatedImages[selectedImage].src;
  //     const selectedTaglineText = selectedTaglines[selectedTagline];

  //     // Use your routing library to redirect to a new page with data
  //     navigate("/merged-content", {
  //       state: { imageURL: selectedImageURL, taglineText: selectedTaglineText },
  //     });
  //   } else {
  //     // Handle the case where no image or tagline is selected (optional: show alert)
  //   }
  // };


  
  const useRedirect = () => {
    const navigate = useNavigate();

    const handleRedirect = (path, state) => {
      navigate(path, state);
    };

    return handleRedirect;
  };

  // const useRedirect = () => {
  //   const navigate = useNavigate(); // Import as needed
  
  //   const handleRedirect = (path, state) => {
  //     navigate(path, state);
  //   };
  
  //   return handleRedirect;
  // };

  // const handleMergeClick = () => {
  //   if (selectedImage !== null && selectedTagline !== null) {
  //     // Get selected image and tagline data
  //     const selectedImageURL = generatedImages[selectedImage].src;
  //     const selectedTaglineText = selectedTaglines[selectedTagline];

  //     // Use your routing library's navigation function
  //     const navigate = useNavigate(); // Assuming React Router DOM
  //     navigate("/merged-content", {
  //       state: { imageURL: selectedImageURL, taglineText: selectedTaglineText },
  //     });
  //   } else {
  //     // Handle the case where no image or tagline is selected (optional: show alert)
  //   }
  //   const redirect = useRedirect();

  //   const navigate = useNavigate(); // Import as needed

  // // const redirect = (path, state) => {
  // //   navigate(path, state);
  // // }; //

  // if (selectedImage !== null && selectedTagline !== null) {
  //   // ... data preparation
  //   const selectedImageURL = generatedImages[selectedImage].src;
  //   const selectedTaglineText = selectedTaglines[selectedTagline];

  //   redirect("/merged-content", { imageURL, taglineText });
  // } else {
  //   // Handle no selection
  // }
  // };

 
  
    const handleMergeClick = () => {
      if (selectedImage !== null && selectedTagline !== null) {
        const selectedImageURL = generatedImages[selectedImage].src;
        const selectedTaglineText = selectedTaglines[selectedTagline];
  
        // Choose redirection approach:
  
        // 1. Using useNavigate directly (requires component conversion)
        // navigate("/merged-content", { state: { imageURL, taglineText } });
  
        // 2. Using custom hook 'useRedirect'
        const redirect = useRedirect();
        redirect("/merged-content", { imageURL, taglineText });
      } else {
        // Handle no selection (optional: show alert)
      }
    };
  
    // ... other event handlers and component logic
  
    
  
 