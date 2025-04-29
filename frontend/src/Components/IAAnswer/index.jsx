import React from "react";
import "./IAAnswer.css";

const IAAnswer = ({ iaAnswer }) => {
    return (
        <div className="ia-container">
            <img width="64" height="64" src="https://img.icons8.com/glyph-neue/64/FFFFFF/message-bot.png" alt="message-bot"/>
            <div className="answer-container">
                <div className="ia-content">{iaAnswer}</div>
            </div>            
        </div>
    );
};

export default IAAnswer;
