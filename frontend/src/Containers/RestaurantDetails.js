import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './RestaurantDetails.css';
import Navbar from '../Components/Navbar';

const RestaurantDetails = () => {
    const { placeId } = useParams();
    const navigate = useNavigate();
    const [restaurant, setRestaurant] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchRestaurantDetails = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    navigate('/login');
                    return;
                }

                console.log('Fetching details for restaurant:', placeId);
                const response = await fetch(
                    `http://localhost:5000/api/restaurants/${placeId}`,
                    {
                        method: 'GET',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        }
                    }
                );

                if (response.ok) {
                    const data = await response.json();
                    console.log('Received restaurant details:', data);
                    setRestaurant(data);
                } else {
                    const errorData = await response.json();
                    console.error('Error response:', errorData);
                    if (response.status === 401) {
                        localStorage.removeItem('token');
                        navigate('/login');
                    } else {
                        setError(errorData.error || 'Failed to fetch restaurant details');
                    }
                }
            } catch (error) {
                console.error('Fetch error:', error);
                setError('An error occurred while fetching restaurant details');
            } finally {
                setLoading(false);
            }
        };

        fetchRestaurantDetails();
    }, [placeId, navigate]);

    if (loading) {
        return (
            <div className="restaurant-details-page">
                <div className="loading">Loading restaurant details...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="restaurant-details-page">
                <div className="error">{error}</div>
            </div>
        );
    }

    if (!restaurant) {
        return (
            <div className="restaurant-details-page">
                <div className="error">Restaurant not found</div>
            </div>
        );
    }

    return (
        <div className="restaurant-details-page">
            <Navbar />
            <div className='restaurant-profile'>
            <div className="restaurant-header-profile">
                <h1>{restaurant.name}</h1>
                <div className="restaurant-meta">
                    <span className="rating">⭐ {restaurant.rating}</span>
                    <span className="price">{'$'.repeat(restaurant.price_level || 1)}</span>
                </div>
            </div>

            <div className="restaurant-info">
                {restaurant.opening_hours && (
                    <div className="hours">
                        <h3>Opening Hours</h3>
                        <div className="hours-list">
                            {restaurant.opening_hours.weekday_text?.map((day, index) => (
                                <p key={index}>{day}</p>
                            ))}
                        </div>
                    </div>
                )}
                <div className="restaurant-profile-right">
                <div className="preferences">
                    <h3>Matched Preferences</h3>
                    <div className="tags">
                        {restaurant.user_preferences?.health_goals?.map((goal, index) => (
                            <span key={index} className="tag health-goal">{goal}</span>
                        ))}
                        {restaurant.user_preferences?.dietary_restrictions?.map((restriction, index) => (
                            <span key={index} className="tag dietary-restriction">{restriction}</span>
                        ))}
                    </div>
                </div>

                {restaurant.website && (
                    <div className="menu-section">
                        <a 
                            href={restaurant.website} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="menu-button-profile"
                        >
                            View Full Menu
                        </a>
                    </div>
                )}
                </div>
            </div>
        </div>
    </div>
    );
};

export default RestaurantDetails; 