import React from "react";
import "./Square.css";

const Square = ({ value, onClick }) => {
    return (
        <div className="square-container" onClick={onClick}>
            <div className="square-text">{value}</div>
        </div>
    );
};

export default Square;
