import logo from './logo.svg';
import './App.css';
import ImageUpload from './ImageUpload';
import Card from './Card';
import { useState } from 'react';
import "./CardList.css"

function App() {

  const [cards, setCards] = useState([])
  const [uploadedImage, setUploadedImage] = useState(null);

  const addNewCard = (data) => {
    const newCard = {
      id: cards.length + 1,
      title: `Card ${data.title}`,
      image: "https://via.placeholder.com/150",
      description: `${data.description}.`,
      releasedate: `${data["release-date"]}.`
    };
    setCards([...cards, newCard])
  }


  const handleUploadSuccess = (responseData) => {
    // Assuming imageData contains the URL of the uploaded image
    //setUploadedImage(imageData.imageUrl); // Update state with uploaded image URL
    console.log("DATA: ", responseData)
    console.log("e", typeof(responseData))
    console.log("Title: ", responseData.title)

    for (const key in responseData) {
      if (responseData.hasOwnProperty(key)) {
          console.log("KEY IS: ", key)
          const value = responseData[key];
          console.log(`${key}: ${typeof value === 'object' ? JSON.stringify(value) : value}`);
      }
  }
    for (const key in responseData) {
      if (responseData.hasOwnProperty(key)) {
        addNewCard(responseData[key]); // Create new card with uploaded image
      }
    }
  };

  /*
          <button onClick={addNewCard} className="add-card-button">
        Add New Card
      </button>
  */


    /*
              <Card 
            key={card.id} 
            title={card.title} 
            image={card.image} 
            description={card.description} 
          />

    */

          /*
          <div key={card.id} className="card">
            <img src={card.image} alt={card.title} className="card-img" />
            <div className="card-content">
              <h2 className="card-title">{card.title}</h2>
              <p className="card-description">{card.description}</p>
            </div>
          </div>
          */

  return (
    <div className="App">
      <header className="App-header">
        <ImageUpload onUploadSuccess={handleUploadSuccess} />
        


        <div className="card-list">
        {cards.map((card) => (
              <Card 
              key={card.id} 
              title={card.title} 
              image={card.image} 
              description={card.description} 
              releasedate={card.releasedate}
            />
        ))}
    </div>



      </header>
    </div>
  );
}

export default App;
