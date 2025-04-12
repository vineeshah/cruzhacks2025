import React from 'react';
import './RestaurantPopUp.css'; 

const RestaurantPopUp = ({ name, cuisine, imageSrc, rating, price, goalsMet }) => {
    return (
        <div className="restaurant-popup">
            <button>
            <img src={imageSrc} alt={name} className="restaurant-image" />
            <div className='restaurant-info'>
                <h3 className="restaurant-name">{name}</h3>
                <div>
                    <div>
                        <h4 className="restaurant-rating">{rating} / 5</h4>
                        <p className="restaurant-cuisine">{cuisine}</p>
                        <p className="restaurant-price">{price}</p>
                    </div>
                <p className="restaurant-goals-met">{goalsMet}</p>
                </div>
            </div>
            </button>
        </div>
    );
};

export default RestaurantPopUp;