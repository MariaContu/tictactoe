import React from "react";
import "./NewGame.css";

const NewGame = ({ onClick }) => {
    return (
        <button className="restart-button" onClick={onClick}>
            Jogar de Novo
        </button>
    );
};

export default NewGame;
