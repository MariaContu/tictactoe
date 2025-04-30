import { useState, useEffect } from 'react';
import Board from './components/Board';
import Dropdown from './components/Dropdown';

const initialBoard = Array(9).fill(null);

function App() {
  const [board, setBoard] = useState(initialBoard);
  const [isXTurn, setIsXTurn] = useState(true);
  const [gameOver, setGameOver] = useState(false);
  const [message, setMessage] = useState('Seu turno!');
  const [modelo, setModelo] = useState('knn');

  const handleClick = async (index) => {
    if (board[index] || gameOver || !isXTurn) return;

    const newBoard = [...board];
    newBoard[index] = 'X';
    setBoard(newBoard);
    setIsXTurn(false);

    await verificarEstadoDoJogo(newBoard);
  };

  const verificarEstadoDoJogo = async (boardAtual) => {
    try {
      const response = await fetch(`http://localhost:5001/prever${modelo}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tabuleiro: boardAtual.map(v => v ? v.toLowerCase() : 'b')
        })
      });

      const data = await response.json();
      const resultado = data.resultado;

      if (resultado === 'Tem jogo') {
        setTimeout(() => iaJoga(boardAtual), 500);
      } else {
        setMessage(resultado);
        setGameOver(true);
      }
    } catch (err) {
      console.error('Erro ao consultar IA:', err);
    }
  };

  const iaJoga = async (boardAtual) => {
    const livres = boardAtual
      .map((v, i) => (v === null ? i : null))
      .filter(v => v !== null);

    if (livres.length === 0 || gameOver) return;

    const randomIndex = livres[Math.floor(Math.random() * livres.length)];
    const newBoard = [...boardAtual];
    newBoard[randomIndex] = 'O';
    setBoard(newBoard);

    const response = await fetch(`http://localhost:5001/prever${modelo}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tabuleiro: newBoard.map(v => v ? v.toLowerCase() : 'b')
      })
    });

    const data = await response.json();
    const resultado = data.resultado;

    if (resultado === 'Tem jogo') {
      setIsXTurn(true);
      setMessage('Seu turno!');
    } else {
      setMessage(resultado);
      setGameOver(true);
    }
  };

  const novoJogo = () => {
    setBoard(initialBoard);
    setIsXTurn(true);
    setGameOver(false);
    setMessage('Seu turno!');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 30 }}>
      <h1>Jogo da Velha com IA</h1>
      <Dropdown modelo={modelo} setModelo={setModelo} />
      <Board board={board} onClick={handleClick} />
      <p>{message}</p>
      <button onClick={novoJogo}>Novo Jogo</button>
    </div>
  );
  
}

export default App;
