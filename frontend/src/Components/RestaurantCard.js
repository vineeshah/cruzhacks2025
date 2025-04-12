import React from 'react';
import './RestaurantCard.css';

const RestaurantCard = ({ restaurant }) => {
    console.log('RestaurantCard received:', restaurant); // Debug log
    
    if (!restaurant) {
        console.error('No restaurant data provided');
        return null;
    }

    return (
        <div className="restaurant-card">
            <div className="restaurant-header">
                <h3>{restaurant.name || 'Unnamed Restaurant'}</h3>
                <div className="restaurant-rating">
                    {restaurant.rating ? `⭐ ${restaurant.rating}` : 'No rating'}
                </div>
            </div>
            <div className="restaurant-address">
                {restaurant.address || restaurant.vicinity || 'Address not available'}
            </div>
            {restaurant.health_analysis && (
                <div className="restaurant-health">
                    <h4>Health Analysis</h4>
                    <ul>
                        {restaurant.health_analysis.map((item, index) => (
                            <li key={index}>
                                <strong>{item.name}</strong>
                                <div>Rating: {item.health_rating}/10</div>
                                <div>{item.explanation}</div>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default RestaurantCard; 