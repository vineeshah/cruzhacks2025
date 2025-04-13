import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Recipe.css';
import Navbar from './Navbar';

const Recipe = () => {
    const navigate = useNavigate();
    const [searchQuery, setSearchQuery] = useState('');
    const [alternatives, setAlternatives] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!searchQuery.trim()) return;
        
        setIsLoading(true);
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/login');
                return;
            }

            console.log('Searching for:', searchQuery);
            const response = await fetch('http://localhost:5000/api/food/recipe-alternatives', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ food_item: searchQuery })
            });

            if (response.status === 401) {
                // Token expired or invalid
                localStorage.removeItem('token');
                navigate('/login');
                return;
            }

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Raw response data:', data);
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            if (!data || !data.alternatives) {
                throw new Error('Invalid response format from server');
            }

            // Transform the data to match the expected format
            const transformedAlternatives = data.alternatives.map(alt => {
                console.log('Processing alternative:', alt);
                return {
                    name: alt.recipe_name || alt.name || 'Unnamed Recipe',
                    description: alt.description || 'No description available',
                    benefits: alt.benefits || 'No health benefits information available',
                    link: alt.link || '#',
                    food_item: alt.food_item || 'Unknown Food Item',
                    user_preferences: data.user_preferences
                };
            });

            setAlternatives(transformedAlternatives);
            console.log('Set alternatives to:', transformedAlternatives);
        } catch (error) {
            console.error('Error:', error);
            setAlternatives([]);
            // You might want to show an error message to the user here
        } finally {
            setIsLoading(false);
        }
    };

    const handleBack = () => {
        navigate(-1);
    };

    return (
        <div className="recipe-card">
            <Navbar />
            <div className="search-section1">
                <h2>Find Healthier Alternatives</h2>
                <form onSubmit={handleSearch} className="search-form">
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="Enter a food item or recipe name..."
                        className="search-input"
                    />
                    <button type="submit" className="search-button" disabled={isLoading}>
                        {isLoading ? 'Searching...' : 'Find Alternatives'}
                    </button>
                </form>
            </div>

            {isLoading && <div className="loading-message">Searching for alternatives...</div>}

            <div className="alternatives-section">
                {alternatives.length > 0 ? (
                    <>
                        <h3>Healthier Alternatives</h3>
                        <div className="alternatives-grid">
                            {alternatives.map((alt, index) => (
                                <div key={index} className="alternative-card">
                                    <div className="recipe-details">
                                        <h3>{alt.name}</h3>
                                        <p>{alt.description}</p>
                                        <div className="health-benefits">
                                            <h4>Health Benefits:</h4>
                                            <p>{alt.benefits}</p>
                                        </div>
                                        <div className="recipe-link">
                                            <a 
                                                href={alt.link} 
                                                target="_blank" 
                                                rel="noopener noreferrer"
                                                className="view-recipe-btn"
                                            >
                                                View Recipe
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </>
                ) : (
                    !isLoading && <div className="no-results">No alternatives found. Try a different search.</div>
                )}
            </div>
        </div>
    );
};

export default Recipe; 