import React, { useState } from "react";
import { Link } from "react-router-dom";

export function Quiz() {
  const questions = [
    {
      questionText: "What background setting would you like for your bottle?",
      answerOptions: [
        { answerText: "City", isCorrect: false },
        { answerText: "Nature", isCorrect: false },
        { answerText: "Indoor", isCorrect: true },
        { answerText: "Outdoor", isCorrect: false },
      ],
    },
    {
      questionText: "What lighting condition would you prefer?",
      answerOptions: [
        { answerText: "Daylight", isCorrect: false },
        { answerText: "Night Light", isCorrect: true },
        { answerText: "Soft Ambient Light", isCorrect: false },
        { answerText: "Random Setting", isCorrect: false },
      ],
    },
    {
      questionText: "Select a surface or prop:",
      answerOptions: [
        { answerText: "Wooden Table", isCorrect: true },
        { answerText: "Glass Table", isCorrect: false },
        { answerText: "Coffee House", isCorrect: false },
        { answerText: "Class Room", isCorrect: false },
      ],
    },
    {
      questionText:
        "Would you like to place additional items with your bottle?",
      answerOptions: [
        { answerText: "Just Alone", isCorrect: false },
        { answerText: "WIth books", isCorrect: false },
        { answerText: "With Lunch Box", isCorrect: false },
        { answerText: "With bag", isCorrect: true },
      ],
    },
    {
      questionText: "What should be the alignment of the bottle?",
      answerOptions: [
        { answerText: "Standing", isCorrect: false },
        { answerText: "Laying down", isCorrect: false },
        { answerText: "Tilted", isCorrect: false },
        { answerText: "Custom", isCorrect: true },
      ],
    },
    {
      questionText: "Choose a season or theme:",
      answerOptions: [
        { answerText: "Summer", isCorrect: false },
        { answerText: "Autumn", isCorrect: false },
        { answerText: "Winter", isCorrect: false },
        { answerText: "Festive (e.g., Christmas, Halloween)", isCorrect: true },
      ],
    },
  ];

  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [showScore, setShowScore] = useState(false);
  const [score, setScore] = useState(0);

  const handleAnswerOptionClick = (isCorrect) => {
    if (isCorrect) {
      setScore(score + 1);
    }

    const nextQuestion = currentQuestion + 1;
    if (nextQuestion < questions.length) {
      setCurrentQuestion(nextQuestion);
    } else {
      // setShowScore(true);
      window.location.href = "http://localhost:3000/";
    }
  };
  // return (
  //   <div>
  //     <div className="app">
  //       {showScore ? (
  //         <div className="score-section">
  //           You scored {score} out of {questions.length}
  //         </div>
  //       ) : (
  //         <>
  //           <div className="question-section">
  //             <div className="question-count">
  //               <span>Question {currentQuestion + 1}</span>/{questions.length}
  //             </div>
  //             <div className="question-text">
  //               {questions[currentQuestion].questionText}
  //             </div>
  //           </div>
  //           <div className="answer-section">
  //             {questions[currentQuestion].answerOptions.map((answerOption) => (
  //               <button className="quizButton"
  //                 onClick={() =>
  //                   handleAnswerOptionClick(answerOption.isCorrect)
  //                 }
  //               >
  //                 {answerOption.answerText}
  //               </button>
  //             ))}
  //           </div>
  //         </>
  //       )}
  //     </div>
  //     <div>
  //       <button className="quizButton" class="submit">Submit</button>
  //     </div>
  //   </div>
  // );

  return (
    <div className="quizbody">
      <div>
        <div className="app">
          {showScore ? (
            <div className="score-section">
              You scored {score} out of {questions.length}
            </div>
          ) : (
            <>
              <div className="question-section">
                <div className="question-count">
                  <span>Question {currentQuestion + 1}</span>/{questions.length}
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
                        handleAnswerOptionClick(answerOption.isCorrect)
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
        {currentQuestion === questions.length - 1 && (
          <div>
            <Link to="/ad">
              <button className="quizButton quizsubmit">Submit</button>
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
