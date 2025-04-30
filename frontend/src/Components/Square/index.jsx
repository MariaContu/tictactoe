import React from "react";
import "./Square.css";

const Square = ({ value, onClick, index }) => {
    return (
        <div className="square-container" onClick={onClick}>
            <div className="square-text">
                {value ?? index}
            </div>
        </div>
    );
};

export default Square;
