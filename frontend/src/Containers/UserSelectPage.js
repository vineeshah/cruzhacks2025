import React, { useState } from 'react';
import Navbar from '../Components/Navbar';
import { useNavigate } from 'react-router-dom';
import './UserSelectPage.css';

const FoodOptionCard = ({ title, description, icon, isSelected, onClick }) => (
    <div 
        className={`food-option-card ${isSelected ? 'selected' : ''}`}
        onClick={onClick}
    >
        <div className="food-icon">{icon}</div>
        <h3>{title}</h3>
        <p>{description}</p>
        {isSelected && <div className="selected-check">✓</div>}
    </div>
);

const UserSelectPage = () => {
    const navigate = useNavigate();
    const [selectedOption, setSelectedOption] = useState(null);

    const foodOptions = [
        {
            id: 'takeout',
            title: "Takeout",
            description: "Find healthy options from restaurants near you",
            icon: "🥡"
        },
        {
            id: 'recipes',
            title: "Home Cooking",
            description: "Discover nutritious recipes you can make at home",
            icon: "👩‍🍳"
        }
    ];

    const handleOptionSelect = (optionId) => {
        setSelectedOption(optionId);
    };

    const handleContinue = () => {
        if (!selectedOption) {
            alert("Please select an option to continue");
            return;
        }

        navigate(`/${selectedOption}`);
    };

    return (
        <div className='user-select-page'>
            <Navbar />
            <div className='user-select-content'>
                <h1>What would you like to eat?</h1>
                <p className="subtitle">Choose your preferred dining option</p>
                <div className="food-options-container">
                    {foodOptions.map((option) => (
                        <FoodOptionCard
                            key={option.id}
                            title={option.title}
                            description={option.description}
                            icon={option.icon}
                            isSelected={selectedOption === option.id}
                            onClick={() => handleOptionSelect(option.id)}
                        />
                    ))}
                </div>
                <button 
                    className={`continue-button ${selectedOption ? 'active' : ''}`}
                    onClick={handleContinue}
                >
                    Continue
                </button>
            </div>
        </div>
    );
};

export default UserSelectPage;