import React, { useRef, useState } from 'react';
import "./Card.css";

const Card = ({ id, title, image, description, release_date, loose_price, complete_price, genre, esrb_rating, publisher, developer, onDelete }) => {
  const [showDescription, setShowDescription] = useState(false);
  const descriptionRef = useRef(null);

  const toggleDescription = () => {
    console.log(id)
    setShowDescription(!showDescription);
  };

  /*
        "genre": "Platformer",
        "release_date": "February 12, 1990",
        "esrb_rating": "Everyone",
        "publisher": "Nintendo",
        "developer": "Nintendo R&D2",

        Genre, ESRB, Publisher, Developer -> might be worth adding
  */

        //some games might miss some of this information
        //RP for games without esrb? such as Dr. Mario NES

        //for listed cards and sold cards, need to include listed date, sold date, listed price, sold price, and purchasedprice
        //also whether it is sold or not.
        //maybe also links for ebay listing and photo of what is it and what you're selling?


  return (
    <div className="card">

      
      <button className="delete-icon" onClick={onDelete}>
        ❌
      </button>
      

      <img src={image} alt={title} className="card-img" />
      <div className="card-content">
        <h2 className="card-title">{title}</h2>
        <h3 className="card-description">id: {id}</h3>
        <h3 className="card-description">Loose Price: {loose_price}</h3>
        <h3 className="card-description">Complete Price: {complete_price}</h3>
        <h3 className="card-description">Release Date: {release_date}</h3>
        <h3 className="card-description">ESRB Rating: {esrb_rating}</h3>
        <h3 className="card-description">Publisher: {publisher}</h3>
        <h3 className="card-description">Developer: {developer}</h3>
        <div
          className="card-description-container"
          style={{
            height: showDescription
              ? `${descriptionRef.current?.scrollHeight || 0}px`
              : '0',
          }}
        >
          <p className="card-description" ref={descriptionRef}>
            {description}
          </p>
        </div>
        <button className="toggle-button" onClick={toggleDescription}>
          {showDescription ? 'Hide Details' : 'Show Details'}
        </button>
      </div>
    </div>
  );
};

export default Card;
