import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { gsap } from 'gsap';
import './Navbar.css';

const Navbar = () => {
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
   
        if (location.state?.from === 'login' || location.state?.from === 'register') {

            gsap.fromTo(
                '.navbar',
                { y: '-100%', opacity: 0 }, 
                { 
                    y: '0%',
                    opacity: 1, 
                    duration: 1, 
                    ease: 'back.out(1.7)',
                    onComplete: () => {
                        
                        navigate(location.pathname, { replace: true });
                    }
                }
            );
        }
    }, [location.state, navigate, location.pathname]);
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
                    <button className="nav-link" onClick={() => navigate('/welcome')}>
                        Health Goals
                    </button>
                    <button className="nav-link" onClick={() => navigate('/user-select')}>
                        Food Options
                    </button>
                    <button className="nav-link logout" onClick={handleLogout}>
                        Logout
                    </button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;