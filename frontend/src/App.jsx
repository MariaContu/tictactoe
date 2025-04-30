import './App.css';
import Square from "./Components/Square";
import IAAnswer from './Components/IAAnswer';
import NewGame from './Components/NewGame';
import { useState, useEffect } from 'react';

function App() {
  const [board, setBoard] = useState(Array(9).fill(null));
  const [isXTurn, setIsXTurn] = useState(true);
  const [iaAnswer, setIaAnswer] = useState('Tem jogo');
  const [gameOver, setGameOver] = useState(false);


  const handleNewGame = () => {
    setBoard(Array(9).fill(null));
    setIsXTurn(true);
    setIaAnswer('Tem jogo');
    setGameOver(false);
  };


  const handleClick = (index) => {
    if (board[index] || gameOver) return; 

    const newBoard = [...board];
    newBoard[index] = 'X';
    setBoard(newBoard);
    setIsXTurn(false);

    setIaAnswer('Tem jogo');
  };


  useEffect(() => {
    if (!isXTurn && !gameOver) {
      const emptyIndices = board
        .map((value, index) => value === null ? index : null)
        .filter((v) => v !== null);
  
      if (emptyIndices.length > 0) {
        const randomIndex = emptyIndices[Math.floor(Math.random() * emptyIndices.length)];
        const newBoard = [...board];
        newBoard[randomIndex] = 'O';
  
        setTimeout(() => {
          setBoard(newBoard);
          setIsXTurn(true);
  
          // Chamada para a IA Flask
          const payload = {
            tabuleiro: newBoard.map(v => v ? v.toLowerCase() : 'b') // 'X' -> 'x', null -> 'b'
          };
  
          fetch('http://localhost:5001/preverknn', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
          })


            .then(res => res.json())
            .then(data => {
              setIaAnswer(data.resultado);
              if (data.resultado !== "Tem jogo") {
                setGameOver(true);
              }
            })
            .catch(err => {
              console.error("Erro ao chamar a IA:", err);
              setIaAnswer("Erro ao consultar IA");
            });
  
        }, 500);
      }
    }
  }, [isXTurn, board, gameOver]);
  

  return (
    <>
      <h3>Tic Tac Toe</h3>
      <IAAnswer iaAnswer={iaAnswer} />
      <div className="board">
        {board.map((value, index) => (
          <Square key={index} value={value} onClick={() => handleClick(index)} />
        ))}
      </div>
      <NewGame onClick={handleNewGame} />
    </>
  );
}

export default App;
