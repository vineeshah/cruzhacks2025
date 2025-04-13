import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import './Navbar.css';

const Navbar = () => {
    const navigate = useNavigate();
    const isAuthenticated = localStorage.getItem('token');

    useEffect(() => {
        const timeout = setTimeout(() => {
            const wavePath = document.querySelector('.wave-path');
            if (wavePath) {
                gsap.to(wavePath, {
                    duration: 6,
                    repeat: -1,
                    yoyo: true,
                    ease: 'power1.inOut',
                    attr: {
                        d: "M0,40 Q120,50 240,40 T480,40 T720,40 T960,40 T1200,40 T1440,40 L1440,0 L0,0 Z"
                    }
                });
            } else {
                console.error('Wave path not found');
            }
        }, 0);
    
        return () => clearTimeout(timeout); // Cleanup timeout
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    return (
        <nav className="navbar">
            <div className="waveNavbar">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 80">
                <path
                    className="wave-path"
                    fill="#ffcccb"
                    d="M0,40 Q120,60 240,40 T480,40 T720,40 T960,40 T1200,40 T1440,40 L1440,0 L0,0 Z"
                ></path>
            </svg>
            </div>
            <div className="navbar-content">
                <div className="navbar-brand">IdealMeal</div>
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
            </div>
        </nav>
    );
};

export default Navbar;