import React from 'react';
import './Homepage.css';
import { useNavigate } from 'react-router-dom';

const Homepage = () => {
    const navigate = useNavigate(); // Initialize the navigate function
    
    return (
        <div className='homepage'>
            <div className='header-homepage'>
                <h1 className='healthify-logo'>
                    Healthify
                </h1>
            </div>
            <div className='content-homepage'>
                <div className='left-homepage'>
                    <h2 className='homepage-text'>
                        Begin your food journey to discover healthy 
                        alternatives matching your preferences.
                    </h2>
                </div>
                <div className='right-homepage'>
                    <button 
                        className='homepage-buttons' 
                        onClick={() => navigate('/signin')} // Navigate to sign-in page
                    >
                        Login
                    </button>
                    <button 
                        className='homepage-buttons' 
                        onClick={() => navigate('/signup')} // Navigate to sign-up page
                    >
                        Sign Up
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Homepage;