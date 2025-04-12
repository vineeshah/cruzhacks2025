import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
    const navigate = useNavigate();
    const isAuthenticated = localStorage.getItem('token');

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/');
    };

    return (
        <nav className="navbar">
            <div className="navbar-brand" onClick={() => navigate('/')}>
                Healthify
            </div>
            
            <div className="navbar-links">
                {isAuthenticated ? (
                    <>
                        <button 
                            className="nav-link"
                            onClick={() => navigate('/welcome')}
                        >
                            Health Goals
                        </button>
                        <button 
                            className="nav-link"
                            onClick={() => navigate('/user-select')}
                        >
                            Food Options
                        </button>
                        <button 
                            className="nav-link"
                            onClick={() => navigate('/takeout')}
                        >
                            Takeout
                        </button>
                        <button 
                            className="nav-link logout"
                            onClick={handleLogout}
                        >
                            Logout
                        </button>
                    </>
                ) : (
                    <>
                        <button 
                            className="nav-link"
                            onClick={() => navigate('/login')}
                        >
                            Login
                        </button>
                        <button 
                            className="nav-link"
                            onClick={() => navigate('/register')}
                        >
                            Register
                        </button>
                    </>
                )}
            </div>
        </nav>
    );
};

export default Navbar; 