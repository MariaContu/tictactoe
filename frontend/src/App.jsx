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
  const [modeloIA, setModeloIA] = useState('knn'); 



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
  };

  const consultarIA = (tabuleiroAtual) => {
    const payload = {
      tabuleiro: tabuleiroAtual.map(v => v ? v.toLowerCase() : 'b')
    };
  
    console.log("Payload enviado para IA:", payload.tabuleiro);
  
    fetch(`http://localhost:5001/prever${modeloIA}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
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
  };
  


  useEffect(() => {
    if (gameOver) return;

    // Sempre que o tabuleiro mudar, consultar a IA
    consultarIA(board);

    // Se for a vez da IA (O), jogar
    if (!isXTurn && !gameOver) {
      const emptyIndices = board
        .map((value, index) => value === null ? index : null)
        .filter((v) => v !== null);

      if (emptyIndices.length > 0 ) {
        const randomIndex = emptyIndices[Math.floor(Math.random() * emptyIndices.length)];
        const newBoard = [...board];
        newBoard[randomIndex] = 'O';

        setTimeout(() => {
          setBoard(newBoard);
          setIsXTurn(true);
        }, 500);
      }
    }
  }, [board, isXTurn, gameOver, modeloIA]);

  return (
    <>
    <div style={{ marginBottom: '10px' }}>
  <label htmlFor="modelo">Modelo IA:&nbsp;</label>
  <select id="modelo" value={modeloIA} onChange={e => setModeloIA(e.target.value)}>
    <option value="knn">KNN</option>
    <option value="mlp">MLP</option>
    <option value="dt">Decision Tree</option>
    <option value="rf">Random Forest</option>
    <option value="xgb">XGBoost</option>
    

  </select>
</div>

      <h3>Tic Tac Toe</h3>
      <IAAnswer iaAnswer={iaAnswer} />
      <div className="board">
        {board.map((value, index) => (
          <Square key={index} value={value} onClick={() => handleClick(index)} index={index} />

        ))}
      </div>
      <NewGame onClick={handleNewGame} />
    </>
  );
}

export default App;
