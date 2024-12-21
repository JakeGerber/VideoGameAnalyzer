import React, { useRef, useState } from 'react';
import "./Card.css";

const Card = ({ title, image, description, releasedate, loose_price, complete_price }) => {
  const [showDescription, setShowDescription] = useState(false);
  const descriptionRef = useRef(null);

  const toggleDescription = () => {
    setShowDescription(!showDescription);
  };

  return (
    <div className="card">
      <img src={image} alt={title} className="card-img" />
      <div className="card-content">
        <h2 className="card-title">{title}</h2>
        <h3 className="card-description">{loose_price}</h3>
        <h3 className="card-description">{complete_price}</h3>
        <h3 className="card-description">{releasedate}</h3>
        <h3 className="card-description">ADD PRICE HERE</h3>
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
