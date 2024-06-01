// Formularz.js

import React, { useState, useEffect } from 'react';

const Formularz = () => {
  const [n, setN] = useState('');
  const [m, setM] = useState('');
  const [popyty, setPopyty] = useState([]);
  const [podazy, setPodazy] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    // Pobierz informacje na temat N i M po załadowaniu komponentu
    fetch('http://127.0.0.1:5000/get_n_m')
      .then(response => response.json())
      .then(data => {
        setN(data.n);
        setM(data.m);
        setPopyty(Array.from({ length: data.n }, (_, index) => ''));
        setPodazy(Array.from({ length: data.m }, (_, index) => ''));
      })
      .catch(error => console.error('Błąd podczas pobierania N i M:', error));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Sprawdź, czy N i M są dodatnimi liczbami
    if (!/^\d+$/.test(n) || !/^\d+$/.test(m) || n <= 0 || m <= 0) {
      setError('N i M muszą być dodatnimi liczbami.');
      return;
    }

    // Sprawdź, czy suma popytu i podaży jest równa
    const sumaPopytu = popyty.reduce((acc, val) => acc + parseInt(val, 10), 0);
    const sumaPodazy = podazy.reduce((acc, val) => acc + parseInt(val, 10), 0);

    if (sumaPopytu !== sumaPodazy) {
      setError('Suma popytu musi być równa sumie podaży.');
      return;
    }

    setError('');

    try {
      const response = await fetch('http://127.0.0.1:5000/endpoint', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ popyty, podazy }),
      });

      if (response.ok) {
        console.log('Dane wysłane pomyślnie!');
      } else {
        console.error('Błąd podczas wysyłania danych.');
      }
    } catch (error) {
      console.error('Błąd podczas wysyłania danych:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>{error && <p style={{ color: 'red' }}>{error}</p>}</div>
      {popyty.map((popyt, index) => (
        <label key={index}>
          Popyt {index + 1}:
          <input
            type="number"
            value={popyt}
            onChange={(e) => setPopyty((prevPopyty) => {
              const newPopyty = [...prevPopyty];
              newPopyty[index] = parseInt(e.target.value, 10);
              return newPopyty;
            })}
          />
        </label>
      ))}
      <br />
      {podazy.map((podaz, index) => (
        <label key={index}>
          Podaż {index + 1}:
          <input
            type="text"
            value={podaz}
            onChange={(e) => setPodazy((prevPodazy) => {
              const newPodazy = [...prevPodazy];
              newPodazy[index] = parseInt(e.target.value, 10);
              return newPodazy;
            })}
          />
        </label>
      ))}
      <br />
      <button type="submit">Zapisz popyt i podaż</button>
    </form>
  );
};

export default Formularz;
