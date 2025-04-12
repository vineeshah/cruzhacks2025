import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './TakeoutPage.css';
import Logo from '../Components/logo';

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

    // Get location when component mounts
    useEffect(() => {
        getLocation();
    }, []);

    // Fetch restaurants when location is available
    useEffect(() => {
        let isMounted = true;

        const fetchRestaurants = async () => {
            if (!location) return;

            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    navigate('/login');
                    return;
                }

                // Fetch restaurants
                const response = await fetch(
                    `http://localhost:5000/api/restaurants/search?lat=${location.lat}&lng=${location.lng}&radius=10`,
                    {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    }
                );

                if (!isMounted) return;

                if (response.ok) {
                    const data = await response.json();
                    console.log(`Found ${data.length} restaurants`);
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
                console.error('Error fetching restaurants:', error);
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
                <Logo />
                <div className="loading">Loading nearby restaurants...</div>
            </div>
        );
    }

    if (locationError) {
        return (
            <div className="takeout-page">
                <Logo />
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
                        <p>Alternatively, you can:</p>
                        <ol>
                            <li>Open your browser settings</li>
                            <li>Search for "Location" or "Site permissions"</li>
                            <li>Find this website in the list</li>
                            <li>Change the location permission to "Allow"</li>
                        </ol>
                    </div>
                    <button className="retry-button" onClick={getLocation}>
                        Try Again
                    </button>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="takeout-page">
                <Logo />
                <div className="error">{error}</div>
            </div>
        );
    }

    return (
        <div className="takeout-page">
            <Logo />
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
                            <div key={restaurant.place_id} className="restaurant-card">
                                <div className="restaurant-header">
                                    <h3>{restaurant.name}</h3>
                                    <div className="restaurant-rating">
                                        {restaurant.rating ? `⭐ ${restaurant.rating}` : 'No rating'}
                                    </div>
                                </div>
                                <div className="restaurant-address">
                                    {restaurant.address}
                                </div>
                                <div className="restaurant-price">
                                    {restaurant.price_level ? '💰'.repeat(restaurant.price_level) : 'Price not available'}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default TakeoutPage;