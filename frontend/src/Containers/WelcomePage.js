import React, { useState } from 'react';
import Logo from '../Components/logo';
import { useNavigate } from 'react-router-dom';
import './WelcomePage.css';

const DietaryGoalCard = ({ goal, description, icon, isSelected, onClick }) => (
    <div 
        className={`dietary-goal-card ${isSelected ? 'selected' : ''}`}
        onClick={onClick}
    >
        <div className="goal-icon">{icon}</div>
        <h3>{goal}</h3>
        <p>{description}</p>
        {isSelected && <div className="selected-check">✓</div>}
    </div>
);

const WelcomePage = () => {
    const navigate = useNavigate();
    const [selectedGoals, setSelectedGoals] = useState([]);

    const dietaryGoals = [
        {
            id: 1,
            goal: "Weight Loss",
            description: "Healthy and sustainable weight management through balanced nutrition",
            icon: "⚖️"
        },
        {
            id: 2,
            goal: "Muscle Gain",
            description: "High-protein options to support muscle growth and recovery",
            icon: "💪"
        },
        {
            id: 3,
            goal: "Heart Health",
            description: "Low-sodium and heart-healthy food choices",
            icon: "❤️"
        },
        {
            id: 4,
            goal: "Plant-Based",
            description: "Vegetarian and vegan options for a plant-based lifestyle",
            icon: "🌱"
        },
        {
            id: 5,
            goal: "Gluten-Free",
            description: "Delicious meals without gluten",
            icon: "🌾"
        },
        {
            id: 6,
            goal: "Low Carb",
            description: "Reduced carbohydrate options for better blood sugar control",
            icon: "🥑"
        },
        {
            id: 7,
            goal: "High Energy",
            description: "Nutrient-rich foods to boost your energy levels",
            icon: "⚡"
        },
        {
            id: 8,
            goal: "Balanced Diet",
            description: "Well-rounded meals with all essential nutrients",
            icon: "🥗"
        }
    ];

    const toggleGoal = (goalId) => {
        setSelectedGoals(prevSelected => {
            if (prevSelected.includes(goalId)) {
                return prevSelected.filter(id => id !== goalId);
            } else {
                return [...prevSelected, goalId];
            }
        });
    };

    const handleContinue = () => {
        if (selectedGoals.length === 0) {
            alert("Please select at least one dietary goal");
            return;
        }
        // You can pass the selected goals to the next page if needed
        navigate('/user-select');
    };

    return (
        <div className='welcome-page'>
            <Logo />
            <div className='welcome-content'>
                <h1>Welcome to Healthify!</h1>
                <p className="subtitle">Select your health goals (choose all that apply)</p>
                <div className="dietary-goals-grid">
                    {dietaryGoals.map((goal) => (
                        <DietaryGoalCard
                            key={goal.id}
                            goal={goal.goal}
                            description={goal.description}
                            icon={goal.icon}
                            isSelected={selectedGoals.includes(goal.id)}
                            onClick={() => toggleGoal(goal.id)}
                        />
                    ))}
                </div>
                <div className="selected-goals-counter">
                    {selectedGoals.length} goals selected
                </div>
                <button 
                    className={`continue-button ${selectedGoals.length > 0 ? 'active' : ''}`}
                    onClick={handleContinue}
                >
                    Continue to Food Options
                </button>
            </div>
        </div>
    );
};

export default WelcomePage; 