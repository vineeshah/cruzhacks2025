import React, { useState } from 'react';
import './UserGoalsPage.css'; 
import Logo from '../Components/logo'; 
import { useNavigate } from 'react-router-dom';

const UserGoalsPage = () => {
    const [inputValue, setInputValue] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [goals, setGoals] = useState([]);
    const [showCustomOption, setShowCustomOption] = useState(false);
    const navigate = useNavigate(); 

    const allSuggestions = ['Low Carb', 'High Protein', 'Vegan', 'Keto', 'Gluten-Free'];

    const handleInputChange = (e) => {
        const value = e.target.value;
        setInputValue(value);

        if (value) {
            const filteredSuggestions = allSuggestions.filter((suggestion) =>
                suggestion.toLowerCase().includes(value.toLowerCase())
            );
            setSuggestions(filteredSuggestions);

            setShowCustomOption(filteredSuggestions.length === 0);
        } else {
            setSuggestions([]);
            setShowCustomOption(false);
        }
    };

    const handleSuggestionClick = (suggestion) => {
        if (!goals.includes(suggestion)) {
            setGoals([...goals, suggestion]);
        }
        setInputValue('');
        setSuggestions([]);
        setShowCustomOption(false);
    };

    const handleCustomOptionClick = () => {
        if (!goals.includes(inputValue)) {
            setGoals([...goals, inputValue]);
        }
        setInputValue('');
        setSuggestions([]);
        setShowCustomOption(false);
    };

    const handleGoalRemove = (goal) => {
        setGoals(goals.filter((g) => g !== goal));
    };

    return (
        <div className='user-goals-page'>
            <Logo />
            <h1>Welcome to Healthify! Let's get started.</h1>
            <p>Please enter any dietary goal(s) you have:</p>
            <form className='user-goals-form' onSubmit={(e) => e.preventDefault()}>
                <input
                    type='text'
                    value={inputValue}
                    onChange={handleInputChange}
                    placeholder='Enter a dietary goal...'
                    className='user-goals-input'
                />
                <button 
                    type='submit' 
                    className='user-goals-submit' 
                    onClick={() => navigate('/user-select')}
                >
                    Done adding goals?
                </button>
                <ul className='suggestions-list'>
                    {suggestions.map((suggestion, index) => (
                        <li
                            key={index}
                            onClick={() => handleSuggestionClick(suggestion)}
                            className='suggestion-item'
                        >
                            {suggestion}
                        </li>
                    ))}
                    {showCustomOption && inputValue && (
                        <li
                            onClick={handleCustomOptionClick}
                            className='suggestion-item custom-option'
                        >
                            Add "{inputValue}"
                        </li>
                    )}
                </ul>
            </form>
            <div className='selected-goals'>
                {goals.map((goal, index) => (
                    <button
                        key={index}
                        className='goal-button'
                        onClick={() => handleGoalRemove(goal)}
                    >
                        {goal} ✖
                    </button>
                ))}
            </div>
        </div>
    );
};

export default UserGoalsPage;