import React from 'react';
import './Homepage.css';
import { useNavigate } from 'react-router-dom';
import Logo from '../Components/logo'; 

const Homepage = () => {
    const navigate = useNavigate(); 
    
    return (

        <div className='homepage-container'>

            <div className='homepage'>
                <Logo />
                <div className='content-homepage'>
                    <div className='left-homepage'>
                        <h2 className='homepage-text'>
                        Begin your food journey and discover healthy 
                        alternatives that match your preferences.
                        </h2>
                    </div>
                    <div className='right-homepage'>
                        <div className='auth-buttons'>
                            <button 
                                className='homepage-buttons' 
                                onClick={() => navigate('/login')}
                            >
                                Login
                            </button>
                            <button 
                                className='homepage-buttons' 
                                onClick={() => navigate('/register')}
                            >
                                Register
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Homepage;