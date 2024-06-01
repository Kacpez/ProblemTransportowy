import React, { useState, useEffect } from 'react';
import Start from './Start.js';
import Home from './Home.js';
import Genetic from './Genetic.js';

const Miasto2 = () => {
  const [formData, setFormData] = useState({
    selectedCity: 'Olkusz',
    coordinates: { x: 50.28, y: 19.56 },
  });

  const [isFormSubmitted, setFormSubmitted] = useState(false);
  const [isFetchButtonClicked, setFetchButtonClicked] = useState(false);
  const [additionalData, setAdditionalData] = useState(null);
  const [isDataFetched, setDataFetched] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:5000/miasto', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        //const responseData = await response.json();
        console.log('Dane wysłane pomyślnie!');
        setFormSubmitted(true);
      } else {
        console.error('Błąd podczas wysyłania danych.');
      }
    } catch (error) {
      console.error('Błąd podczas wysyłania danych:', error);
    }
  };

  const handleFetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/miasto');
      if (response.ok) {
        const responseData = await response.json();
        setAdditionalData(responseData);
        setDataFetched(true);
      } else {
        console.error('Błąd podczas pobierania danych.');
      }
    } catch (error) {
      console.error('Błąd podczas pobierania danych:', error);
    }
  };

  const handleRetry = () => {
    setFormSubmitted(false);
    setFetchButtonClicked(false);
    setAdditionalData(null);
    setDataFetched(false);
  };

  useEffect(() => {
    if (isDataFetched) {
 
    }
  }, [isDataFetched]);

  return (
    <div>
        <div className="Home"><h1>Zagadnienie transportowe</h1></div>
      {isFormSubmitted ? (
        <div className=" m-3">
            <div className="position-absolute top-20 start-0 m-3">
            <h3>{formData.selectedCity}</h3>
            </div>
         <button  class="btn btn-success btn-lg btn-block" onClick={() => { handleFetchData(); setFetchButtonClicked(true); }}>Pokaż rozwiązanie</button>
      
<div className="position-absolute top-0 end-0 m-3">
         <button class="btn btn-dark btn-lg btn-block" onClick={handleRetry}>Zmień miasto</button>
         </div></div>
      ) : (
        <form onSubmit={handleSubmit}>
          <label>
            Wprowadź miasto:
            <input
              type="text"
              class="form-control"
              name="selectedCity"
              value={formData.selectedCity}
              onChange={handleInputChange}
            />
          </label>
          <div class="alert alert-warning">Najlpiej podać średniej wielkości miasto z liczbą ludności nie przekraczającą 50 tys. oraz z liczbą piekarni i kawiarni do 20.</div>
          <button type="submit" class="btn btn-info">Zapisz</button>
        </form>
      )}
      {isFetchButtonClicked && additionalData && (
        <div>
          <Start x={additionalData["coordinaties"][0]} y={additionalData["coordinaties"][1]} />
          <Home x={additionalData["coordinaties"][0]} y={additionalData["coordinaties"][1]} />
        <Genetic x={additionalData["coordinaties"][0]} y={additionalData["coordinaties"][1]} />
        </div>
      )}
    </div>
  );
};

export default Miasto2;
