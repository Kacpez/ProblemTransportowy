import React, { useState } from 'react';
import Begin from '../components/Start.js';
import Home from '../components/Home.js';
import Genetic from '../components/Genetic.js'
const Miasto = () => {
  const [formData, setFormData] = useState({
    selectedCity: 'Olkusz',
    coordinates: { x: 50.28, y: 19.56 },
  });

  const [isFormSubmitted, setFormSubmitted] = useState(false);

  const handleSelectChange = (e) => {
    const { value } = e.target;

    let coordinates = { x: 50.28, y: 19.56 };

    if (value === 'Olkusz') {
      coordinates = { x: 50.28, y: 19.56 };
    } else if (value === 'Nowy Sącz') {
      coordinates = { x: 49.61, y: 20.71 };
    } else if (value === 'Wieliczka') {
      coordinates = { x: 49.98, y: 20.06 };
    }

    setFormData({ selectedCity: value, coordinates });
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
        console.log('Dane wysłane pomyślnie!');
        setFormSubmitted(true);
      } else {
        console.error('Błąd podczas wysyłania danych.');
      }
    } catch (error) {
      console.error('Błąd podczas wysyłania danych:', error);
    }
  };

  const handleRetry = () => {

    setFormSubmitted(false);
  };

  return (
    <div>
      {isFormSubmitted ? (
        <div>
          <Begin x={formData.coordinates.x} y={formData.coordinates.y} />
          <Home x={formData.coordinates.x} y={formData.coordinates.y} />
          <Genetic x={formData.coordinates.x} y={formData.coordinates.y} />
          <button onClick={handleRetry}>Spróbuj ponownie</button>
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          <label>
            Wybierz miasto:
            <select
              name="miasto"
              value={formData.selectedCity}
              onChange={handleSelectChange}
            >
              <option disabled={true} value="">
                Wybierz miasto
              </option>
              <option value="Olkusz">Olkusz</option>
              <option value="Nowy Sącz">Nowy Sącz</option>
              <option value="Wieliczka">Wieliczka</option>
            </select>
          </label>
          <br />

          <button type="submit">Wyślij</button>
        </form>
      )}
    </div>
  );
};

export default Miasto;
