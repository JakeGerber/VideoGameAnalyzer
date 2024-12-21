import logo from './logo.svg';
import './App.css';
import ImageUpload from './ImageUpload';
import Card from './Card';
import { useState } from 'react';
import "./CardList.css"
import axios from 'axios';

import Camera from './Camera';

function App() {

  const [cards, setCards] = useState([])
  const [uploadedImage, setUploadedImage] = useState(null);
  const [photoUrl, setPhotoUrl] = useState(null);

  const handleCapture = (url) => {
    console.log("Captured URL:", url);
    setPhotoUrl(url);
    console.log("ITS SET: ", url)
  };

  const uploadCameraCapture = () => {
    console.log("Captured URL:", photoUrl);
  }


  const handleUploadCapture = async () => {
    if (!photoUrl) {
      alert("Please select a file first!");
      return;
    }

    console.log(photoUrl)
    
    const base64ToBlob = (base64) => {
      const byteString = atob(base64.split(",")[1]); // Decode base64
      const mimeString = base64.split(",")[0].split(":")[1].split(";")[0]; // Extract MIME type
      const byteArray = new Uint8Array(byteString.length);
  
      for (let i = 0; i < byteString.length; i++) {
        byteArray[i] = byteString.charCodeAt(i);
      }
  
      return new Blob([byteArray], { type: mimeString });
    };
  
    const imageBlob = base64ToBlob(photoUrl);
  
    const formData = new FormData();
    formData.append("image", imageBlob, "image.jpg");
  

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("Upload successful:", response.data);

      handleUploadSuccess(response.data)



    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };


  //complete_price, genre, esrb_rating, publisher, developer

  const addNewCard = (data) => {
    const newCard = {
      id: cards.length + 1,
      title: `${data.title}`,
      image: "https://via.placeholder.com/150",
      description: `${data.description}`,
      release_date: `${data["release_date"]}`,
      loose_price: `${data["loose_price"]}`,
      complete_price: `${data["complete_price"]}`,
      genre: `${data["genre"]}`,
      esrb_rating: `${data["esrb_rating"]}`,
      publisher: `${data["publisher"]}`,
      developer: `${data["developer"]}`,
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

//genre, esrb_rating, publisher, developer

  return (
    <div className="App">
      <header className="App-header">

      <Camera onCapture={handleCapture} />
      <button onClick={handleUploadCapture}>THIS IS FOR SUBMITTING PHOTO CAPTURE</button>


        <ImageUpload onUploadSuccess={handleUploadSuccess} />

        
        


        <div className="card-list">
        {cards.map((card) => (
              <Card 
              key={card.id} 
              title={card.title} 
              image={card.image} 
              description={card.description} 
              release_date={card.release_date}
              loose_price={card.loose_price}
              complete_price={card.complete_price}
              genre={card.genre}
              esrb_rating={card.esrb_rating}
              publisher={card.publisher}
              developer={card.developer}
            />
        ))}
    </div>



      </header>
    </div>
  );
}

export default App;
