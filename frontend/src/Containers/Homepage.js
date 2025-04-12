import React from 'react';
import './Homepage.css';
import { useNavigate } from 'react-router-dom';
import Logo from '../Components/logo'; 

const Homepage = () => {
    const navigate = useNavigate(); 
    
    return (
        <div className='homepage'>
            <Logo />
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
                        onClick={() => navigate('/signin')} // change this so it goes to google sign in
                    >
                        Login
                    </button>
                    <button 
                        className='homepage-buttons' 
                        onClick={() => navigate('/signup')} // same thing as previous comment 
                    >
                        Sign Up
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Homepage;