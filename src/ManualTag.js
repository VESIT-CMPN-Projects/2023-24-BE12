import React, { useState } from 'react';
import './ManualTag.css';

function ManualTag() {
  const [textSize, setTextSize] = useState('16px');
  const [textStyle, setTextStyle] = useState('normal');
  const [textColor, setTextColor] = useState('black');
  const [textBoxes, setTextBoxes] = useState([]);
  const [textInput, setTextInput] = useState('');
  
  const handleTextSizeChange = (e) => {
    setTextSize(e.target.value);
  };

  const handleTextStyleChange = (e) => {
    setTextStyle(e.target.value);
  };

  const handleTextColorChange = (e) => {
    setTextColor(e.target.value);
  };

  const handleInputChange = (e) => {
    setTextInput(e.target.value);
  };

  const handleAddTextBox = (e) => {
    e.preventDefault();
    if (textInput.trim() !== '') {
      setTextBoxes([
        ...textBoxes,
        { text: textInput, position: { top: 100, left: 100 } },
      ]);
      setTextInput('');
    }
  };

  const handleTextBoxDrag = (index, e) => {
    const newTextBoxes = [...textBoxes];
    newTextBoxes[index].position = {
      top: e.clientY - 50,
      left: e.clientX - 50,
    };
    setTextBoxes(newTextBoxes);
  };

  return (
    <div className="manual-tag__container">
      <div className="manual-tag__toolbar">
        <label htmlFor="text-size">Text Size:</label>
        <input
          type="range"
          id="text-size"
          min="12"
          max="36"
          value={textSize}
          onChange={handleTextSizeChange}
        />
        <label htmlFor="text-style">Text Style:</label>
        <select id="text-style" value={textStyle} onChange={handleTextStyleChange}>
          <option value="normal">Normal</option>
          <option value="italic">Italic</option>
        </select>
        <label htmlFor="text-color">Text Color:</label>
        <input
          type="color"
          id="text-color"
          value={textColor}
          onChange={handleTextColorChange}
        />
      </div>
      <div className="manual-tag__image-container">
        <img src="src\masks\mask (1).png" alt="Your Image" />
        {textBoxes.map((box, index) => (
          <div
            key={index}
            className="manual-tag__text-box"
            style={{
              top: box.position.top,
              left: box.position.left,
              fontSize: textSize,
              fontStyle: textStyle,
              color: textColor,
            }}
            draggable
            onDrag={(e) => handleTextBoxDrag(index, e)}
          >
            {box.text}
          </div>
        ))}
      </div>
      <form className="manual-tag__add-text-form" onSubmit={handleAddTextBox}>
        <input
          type="text"
          value={textInput}
          onChange={handleInputChange}
          placeholder="Enter text"
        />
        <button type="submit">Add Text</button>
      </form>
    </div>
  );
}

export default ManualTag;
