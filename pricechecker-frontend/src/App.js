import logo from './logo.svg';
import './App.css';
import ImageUpload from './ImageUpload';
import Card from './Card';
import { useState } from 'react';

function App() {

  const [cards, setCards] = useState([])

  const addNewCard = () => {
    const newCard = {
      id: cards.length + 1,
      title: `Card ${cards.length + 1}`,
      image: "https://via.placeholder.com/150",
      description: `This is the new card description.`
    };
    setCards([...cards, newCard])
  }

  return (
    <div className="App">
      <header className="App-header">
        <ImageUpload />
        
        <button onClick={addNewCard} className="add-card-button">
        Add New Card
      </button>

        <div className="card-list">
        {cards.map((card) => (
          <div key={card.id} className="card">
            <img src={card.image} alt={card.title} className="card-img" />
            <div className="card-content">
              <h2 className="card-title">{card.title}</h2>
              <p className="card-description">{card.description}</p>
            </div>
          </div>
        ))}
    </div>



      </header>
    </div>
  );
}

export default App;
