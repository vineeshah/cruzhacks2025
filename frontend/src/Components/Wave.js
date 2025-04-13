import React, { useEffect } from 'react';
import { gsap } from 'gsap';
import './Wave.css';

const Wave = () => {
    useEffect(() => {
        const wavePath = document.querySelector('.diagonal-wave path');
        gsap.to(wavePath, {
            duration: 5, 
            repeat: -1, 
            yoyo: true, 
            ease: 'power1.inOut',
            attr: {
                d: "M0,40 Q120,60 240,40 T480,60 T720,40 T960,60 T1200,40 T1440,60 L1440,280 Q1320,260 1200,280 T960,260 T720,280 T480,260 T240,280 T0,260 Z"
            }
        });
    }, []);

    return (
        <div className="diagonal-wave">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
                <path
                    fill="#ffcccb"
                    fillOpacity="1"
                    d="M0,40 Q120,80 240,40 T480,40 T720,40 T960,40 T1200,40 T1440,40 L1440,280 Q1320,240 1200,280 T960,280 T720,280 T480,280 T240,280 T0,280 Z"
                ></path>
            </svg>
        </div>
    );
};

export default Wave;