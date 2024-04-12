import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Helmet } from "react-helmet";
import "./home.css";

export function Quiz() {
  const questions = [
    {
      questionText: "Which color scheme aligns best with the desired aesthetic for your soap bar advertisement?",
      answerOptions: [
        { answerText: "Coral pink and golden accents", isCorrect: false },
        { answerText: "Mauve and golden accents", isCorrect: false },
        { answerText: "Light green with green accents", isCorrect: true },
        { answerText: "Light blue with blue accents", isCorrect: false },
      ],
    },
    {
      questionText: "When considering the scent profile, which aroma aligns best with your design vision?",
      answerOptions: [
        { answerText: "Coconut Milk and Jasmine Petals", isCorrect: false },
        { answerText: "Shea Butter and Vanilla", isCorrect: true },
        { answerText: "Lavender and Chamomile", isCorrect: false },
        { answerText: "Cherry and Chia Milk", isCorrect: false },
      ],
    },
    {
      questionText: "What mood or theme should the packaging's design convey?",
      answerOptions: [
        { answerText: "Refreshing and Hydrating", isCorrect: true },
        { answerText: "Exotic and Pampering", isCorrect: false },
        { answerText: "Calming and Relaxing", isCorrect: false },
        { answerText: "Energizing and Revitalizing", isCorrect: false },
      ],
    },
    {
      questionText:
        "What background design do you prefer for the packaging?",
      answerOptions: [
        { answerText: "Plain white background", isCorrect: false },
        { answerText: "Gradient color background", isCorrect: false },
        { answerText: "White background with texture", isCorrect: false },
        { answerText: "Background with a specific color related to the scent or feature", isCorrect: true },
      ],
    },
    {
      questionText: "What textual information is crucial for your packaging?",
      answerOptions: [
        { answerText: "Product name with scent or key ingredient (e.g.,PURELY pampering shea & vanilla)", isCorrect: false },
        { answerText: "The main feature or benefit (e.g., for soft, smooth skin)", isCorrect: false },
        { answerText: "Additional benefits or features (e.g., anti-stress, fragrance free, hypoallergenic)", isCorrect: false },
        { answerText: "Promotional offers (e.g., Buy 4 Get 1 FREE)", isCorrect: true },
      ],
    },
    {
      questionText: "Do you want (Loofah) additional item to be generated with your product?",
      answerOptions: [
        { answerText: "Yes", isCorrect: false },
        { answerText: "No", isCorrect: false },
      ],
    },
  ];

  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [showScore, setShowScore] = useState(false);
  const [score, setScore] = useState(0);
  const [userAnswers, setUserAnswers] = useState([]);

  const handleAnswerOptionClick = (answerText) => {
    const updatedAnswers = [...userAnswers, answerText];
    setUserAnswers(updatedAnswers);

    // Store all answers
    localStorage.setItem("userAnswers", JSON.stringify(updatedAnswers));

    // Store the last answer separately
    localStorage.setItem("lastAnswer", answerText);

    const nextQuestion = currentQuestion + 1;
    if (nextQuestion < questions.length) {
      setCurrentQuestion(nextQuestion);
    } else {
      setShowScore(true);
    }
  };
  
  
  
  const handlePreviousQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  return (
    <div>
      <div className="home-header" style={{ color: "black" }}>
        <header
          style={{ color: "black" }}
          data-thq="thq-navbar"
          className="navbarContainer home-navbar-interactive"
        >
          <span className="logo">ADGENAI</span>
          <div
            data-thq="thq-mobile-menu"
            className="home-mobile-menu1 mobileMenu"
          >
            <div className="home-nav">
              <div className="home-top">
                <span className="logo">ADGENAI</span>
              </div>
            </div>
            <div>
            </div>
          </div>
        </header>
      </div>
      <div className="quizbody">
        <div>
          <div className="app">
            {showScore ? (
              <div className="score-section">
                Questionnaire Done!
                <Link to="/ad">
                  <button className="quizButton quizsubmit">Submit</button>
                </Link>
              </div>
            ) : (
              <>
                <div className="question-section">
                  <div className="question-count">
                    <span>Question {currentQuestion + 1}</span>/
                    {questions.length}
                  </div>
                  <div className="question-text">
                    {questions[currentQuestion].questionText}
                  </div>
                </div>
                <div className="answer-section">
                  {questions[currentQuestion].answerOptions.map(
                    (answerOption) => (
                      <button
                        className="quizButton"
                        key={answerOption.answerText}
                        onClick={() =>
                          handleAnswerOptionClick(answerOption.answerText)
                        }
                      >
                        {answerOption.answerText}
                      </button>
                    )
                  )}
                </div>
              </>
            )}
          </div>
        </div>
      </div>
      <div className="button-section">
        <div>
          {currentQuestion > 0 && (
            <button className="quizButton1" onClick={handlePreviousQuestion}>
              Previous
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
