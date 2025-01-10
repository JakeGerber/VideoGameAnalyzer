import logo from "./logo.svg";
import "./App.css";
import ImageUpload from "./ImageUpload";
import Card from "./Card";
import { useState, useEffect } from "react";
import "./CardList.css";
import "./CircleIcon.css"
import "./TextBox.css"
import "./SubmitButton.css"
import axios from "axios";

import Camera from "./Camera";

import { v4 as uuidv4 } from 'uuid';

import LeafletMap from "./LeafletMap";

import IconList from "./IconList";

function App() {

  //cards variable keeps track of the Cards which contain game Information
  const [cards, setCards] = useState(() => {
    //Initialize cards with localStorage if available
    const savedCards = localStorage.getItem('cards');
    if (savedCards)
    {
      return JSON.parse(savedCards)
    }
    else
    {
      return []
    }
  });

  //Save cards to localStorage whenever cards changes
  useEffect(() => {
    localStorage.setItem('cards', JSON.stringify(cards));
  }, [cards]);

  const [photoUrl, setPhotoUrl] = useState(null);

  const [textBoxEntry, setTextBoxEntry] = useState("")
  const [selectedConsole, setSelectedConsole] = useState("nes")

  const [searchResult, setSearchResult] = useState([])

  const handleClickSearchResult = async (item) => {
    //alert(`You selected: ${item}`);
    setTextBoxEntry("")
    setSearchResult([]);
  
    try {
      //Create a FormData object
      const formData = new FormData();
      
      //Append text to form data
      formData.append("text", item);  
    
      //Make post request to backend.
      const response = await axios.post(
        "http://127.0.0.1:5000/upload_title",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
    
      console.log("Upload successful:", response.data);
      addNewCard(response.data[item]);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  //Select console from list
  const handleSelectedConsole = (event) => {
    setSelectedConsole(event.target.value);
  };

  const newTextEntered = (event) => {
    setTextBoxEntry(event.target.value)
  }

  const handleCapture = (url) => {
    console.log("Captured URL:", url);
    setPhotoUrl(url);
    console.log("ITS SET: ", url);
  };

  const uploadCameraCapture = () => {
    console.log("Captured URL:", photoUrl);
  };

  const handleTextUpload = async () => {
    if (textBoxEntry == "")
    {
      alert("Please enter text!");
      return;
    }



    try {
      // Create a FormData object
      const formData = new FormData();
      
      // Append the plain text to the form data
      formData.append("text", textBoxEntry);
      formData.append("console", selectedConsole);

    
      // Make the POST request
      const response = await axios.post(
        "http://127.0.0.1:5000/upload_text",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
    
      // Handle the successful upload
      console.log("Upload successful:", response.data);
      handleUploadTextSuccess(response.data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
    



  }

  const handleUploadCapture = async () => {
    if (!photoUrl) {
      alert("Please select a file first!");
      return;
    }

    console.log(photoUrl);

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
      const response = await axios.post(
        "http://127.0.0.1:5000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log("Upload successful:", response.data);

      handleUploadSuccess(response.data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  //complete_price, genre, esrb_rating, publisher, developer

  const addNewCard = (data) => {
    const newCard = {
      id: `${uuidv4()}`,
      title: `${data.title}`,
      //image: "https://via.placeholder.com/150",
      image: `${data["cover-link"]}`,
      description: `${data.description}`,
      release_date: `${data["release_date"]}`,
      loose_price: `${data["loose_price"]}`,
      complete_price: `${data["complete_price"]}`,
      genre: `${data["genre"]}`,
      esrb_rating: `${data["esrb_rating"]}`,
      publisher: `${data["publisher"]}`,
      developer: `${data["developer"]}`,
    };
    setCards([...cards, newCard]);
  };


  const handleUploadTextSuccess = (responseData) => {
    console.log("RESPONSE DATA!: ", responseData);
    setSearchResult(responseData.text)
    console.log("wow")
    console.log(searchResult)
  }

  const handleUploadSuccess = (responseData) => {
    // Assuming imageData contains the URL of the uploaded image
    //setUploadedImage(imageData.imageUrl); // Update state with uploaded image URL
    console.log("DATA: ", responseData);
    console.log("e", typeof responseData);
    console.log("Title: ", responseData.title);

    for (const key in responseData) {
      if (responseData.hasOwnProperty(key)) {
        console.log("KEY IS: ", key);
        const value = responseData[key];
        console.log(
          `${key}: ${typeof value === "object" ? JSON.stringify(value) : value}`
        );
      }
    }
    for (const key in responseData) {
      if (responseData.hasOwnProperty(key)) {
        addNewCard(responseData[key]); // Create new card with uploaded image
      }
    }
  };

  const handleDeleteCard = (id) => {
    setCards((prevCards) => prevCards.filter((card) => card.id !== id));
  };


  //genre, esrb_rating, publisher, developer
  

  //add search bar with fuzzy search?
  //fuze?

  return (
    <div className="App">
      <header className="App-header">
        <Camera onCapture={handleCapture} />
        <button onClick={handleUploadCapture}>
          THIS IS FOR SUBMITTING PHOTO CAPTURE
        </button>

        <ImageUpload onUploadSuccess={handleUploadSuccess} />

        <img src="/images/camera.png" alt="Example" className="card-img" />


        <div className="card-list">
          {cards.map((card) => (
            <Card
              key={card.id}
              id={card.id}
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
              onDelete = {() => handleDeleteCard(card.id)}
            />
          ))}
        </div>

        <h1>Search By Title:</h1>

        <input type="text" value={textBoxEntry} onChange={newTextEntered} className="professional-input" placeholder="Type something..."/>


        <IconList />








        {searchResult && searchResult.length > 0 && (
        <div
          style={{
            top: "45px",
            left: "0",
            width: "300px",
            border: "1px solid #ccc",
            borderRadius: "4px",
            zIndex: 1000,
            boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
          }}
        >
          {searchResult.map((item, index) => (
            <div
              key={index}
              onClick={() => handleClickSearchResult(item)}
              style={{
                padding: "10px",
                cursor: "pointer",
                borderBottom:
                  index !== searchResult.length - 1
                    ? "1px solid #eee"
                    : "none",
                hover: { backgroundColor: "#f0f0f0" },
              }}
            >
              {item.replace('|', ' - ')}
            </div>
          ))}
          </div>
        )}





        {/*I need to have some sort of dropdown to allow users to select the console*/}
        {/*The issue is that the list will get very long very fast*/}

        <div className="form-item">
      <label className="label">
        Console:
        <select
          name="console"
          value={selectedConsole}
          onChange={handleSelectedConsole}
        >
          <option value="nes">NES</option>
          <option value="super-nintendo">Super Nintendo</option>
          <option value="nintendo-64">Nintendo 64</option>
          <option value="playstation">PlayStation</option>
        </select>
      </label>
    </div>


        <button onClick={handleTextUpload} className="submit-button">Submit textboxentry</button>

        <div>
        <h1>Leaflet Map Example</h1>
        <LeafletMap />
      </div>


      </header>
    </div>
  );
}

export default App;


/*
      <div class="form-item">
        <label class="label">
          Importance:
          <select
            name="importance"
            value={formData.importance}
            onChange={handleChange}
          >
            <option value="none">None</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </label>
      </div>

*/