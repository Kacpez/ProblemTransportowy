import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Wybor = () => {
  const [selectedOption, setSelectedOption] = useState(null);

  const handleOptionChange = (option) => {
    setSelectedOption(option);
  };

  return (
    <div>
      <h2>Wybierz rodzaj optymalizacji:</h2>
        <button onClick={() => handleOptionChange('algorithm')}>Algorytm Optymalizacji</button>
     

        <button onClick={() => handleOptionChange('genetic')}>Algorytm Genetyczny</button>
    
    </div>
  );
};

export default Wybor;
