import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './TakeoutPage.css';
import Navbar from '../Components/Navbar';

const RestaurantCard = ({ restaurant }) => {
    console.log('RestaurantCard received:', restaurant);
    return (
        <Link 
            to={`/restaurants/${restaurant.place_id}`}
            className="restaurant-card-link"
        >
            <div className="restaurant-card">
                <div className="restaurant-header">
                    <h3>{restaurant.name}</h3>
                    <div className="restaurant-rating">
                    <p className="restaurant-address">{restaurant.address}</p>
                        <div>
                            <span className='ratingSpan'>⭐ {restaurant.rating}</span>
                            <span>{'$'.repeat(restaurant.price_level || 1)}</span>
                        </div>
                    </div>
                </div>
                
                <div className="restaurant-details">
                    <div className="health-score">
                        <h4>Health Score: {restaurant.health_score}/100</h4>
                        <div className="tags">
                            {restaurant.health_keywords?.map((keyword, index) => (
                                <span key={index} className="tag health-keyword">{keyword}</span>
                            ))}
                        </div>
                    </div>
                    
                    <div className="user-preferences">
                        <h4>Your Preferences:</h4>
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
                        <div className="menu-link">
                            <a 
                                href={restaurant.website} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="menu-button"
                            >
                                View Menu
                            </a>
                        </div>
                    )}
                </div>
            </div>
        </Link>
    );
};

const TakeoutPage = () => {
    const navigate = useNavigate();
    const [restaurants, setRestaurants] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [location, setLocation] = useState(null);
    const [locationError, setLocationError] = useState('');

    const getLocation = () => {
        setLoading(true);
        setLocationError('');
        
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    setLocation({
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    });
                    setLocationError('');
                },
                (error) => {
                    let errorMessage = 'Unable to get your location. ';
                    switch (error.code) {
                        case error.PERMISSION_DENIED:
                            errorMessage += 'Location access was denied. ';
                            break;
                        case error.POSITION_UNAVAILABLE:
                            errorMessage += 'Location information is unavailable. ';
                            break;
                        case error.TIMEOUT:
                            errorMessage += 'Location request timed out. ';
                            break;
                        default:
                            errorMessage += 'An unknown error occurred. ';
                    }
                    errorMessage += '\n\nTo enable location services:';
                    setLocationError(errorMessage);
                    setLoading(false);
                },
                {
                    enableHighAccuracy: true,
                    timeout: 5000,
                    maximumAge: 0
                }
            );
        } else {
            setLocationError('Geolocation is not supported by your browser.');
            setLoading(false);
        }
    };

    useEffect(() => {
        getLocation();
    }, []);

    useEffect(() => {
        let isMounted = true;

        const fetchRestaurants = async () => {
            if (!location) {
                console.log('Location not available yet');
                return;
            }

            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    navigate('/login');
                    return;
                }

                const response = await fetch(
                    `http://localhost:5000/api/restaurants/search?lat=${location.lat}&lng=${location.lng}&radius=4000`,
                    {
                        method: 'GET',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        }
                    }
                );

                if (!isMounted) return;

                if (response.ok) {
                    const data = await response.json();
                    if (Array.isArray(data) && data.length > 0) {
                        setRestaurants(data);
                    } else {
                        setError('No restaurants found in your area. Try increasing the search radius.');
                    }
                } else {
                    const errorData = await response.json();
                    setError(errorData.error || 'Failed to fetch restaurants');
                }
            } catch (error) {
                if (!isMounted) return;
                setError('An error occurred while fetching restaurants');
            } finally {
                if (isMounted) {
                    setLoading(false);
                }
            }
        };

        fetchRestaurants();

        return () => {
            isMounted = false;
        };
    }, [location, navigate]);

    if (loading && !locationError) {
        return (
            <div className="takeout-page">
                <Navbar />
                <div className="loading">Loading nearby restaurants...</div>
            </div>
        );
    }

    if (locationError) {
        return (
            <div className="takeout-page">
                <Navbar />
                <div className="error">
                    {locationError}
                    <div className="location-help">
                        <p>To enable location services:</p>
                        <ol>
                            <li>Click the three dots (⋮) or lock icon in your browser's address bar</li>
                            <li>Go to "Settings" or "Site settings"</li>
                            <li>Find "Location" in the permissions list</li>
                            <li>Change the setting to "Allow"</li>
                            <li>Refresh this page</li>
                        </ol>
                    </div>
                </div>
                <button className="retry-button" onClick={getLocation}>
                    Try Again
                </button>
            </div>
        );
    }

    if (error) {
        return (
            <div className="takeout-page">
                <Navbar />
                <div className="error">{error}</div>
            </div>
        );
    }

    return (
        <div className="takeout-page">
            <Navbar />
            <div className="takeout-content">
                <h1>Nearby Restaurants</h1>
                <p className="subtitle">Find healthy options near you</p>
                
                {loading ? (
                    <div className="loading">Loading nearby restaurants...</div>
                ) : error ? (
                    <div className="error">{error}</div>
                ) : restaurants.length === 0 ? (
                    <div className="no-restaurants">
                        No restaurants found in your area. Try increasing the search radius.
                    </div>
                ) : (
                    <div className="restaurants-grid">
                        {restaurants.map((restaurant) => (
                            <RestaurantCard key={restaurant.place_id} restaurant={restaurant} />
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default TakeoutPage;