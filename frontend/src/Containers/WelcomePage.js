import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import './WelcomePage.css';
import Navbar from '../Components/Navbar';

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
    const [error, setError] = useState('');

    const dietaryGoals = useMemo(() => [
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
    ], []);

    useEffect(() => {
        const fetchUserGoals = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    navigate('/login');
                    return;
                }

                const response = await fetch('http://localhost:5000/api/user/profile', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.health_goals && Array.isArray(data.health_goals)) {
                        setSelectedGoals(data.health_goals);
                    }
                }
            } catch (error) {
                console.error('Error fetching user goals:', error);
            }
        };

        fetchUserGoals();
    }, [navigate]); 

    const toggleGoal = (goalId) => {
        setSelectedGoals(prevSelected => {
            const goal = dietaryGoals.find(g => g.id === goalId);
            if (!goal) return prevSelected;
            
            if (prevSelected.includes(goal.goal)) {
                return prevSelected.filter(name => name !== goal.goal);
            } else {
                return [...prevSelected, goal.goal];
            }
        });
    };

    const handleContinue = async () => {
        if (selectedGoals.length === 0) {
            setError("Please select at least one dietary goal");
            return;
        }

        try {
            const token = localStorage.getItem('token');
            if (!token) {
                setError("Please login to continue");
                navigate('/login');
                return;
            }

            
            const response = await fetch('http://localhost:5000/api/user/preferences', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    health_goals: selectedGoals
                })
            });

            const data = await response.json();

            if (response.ok) {
                navigate('/user-select');
            } else {
                setError(data.error || "Failed to save preferences. Please try again.");
            }
        } catch (error) {
            console.error('Error saving preferences:', error);
            setError("An error occurred. Please try again.");
        }
    };

    return (
        <div className='welcome-page'>
            <Navbar />
            <div className='welcome-content'>
                <h1>Welcome to IdealMeal!</h1>
                <p className="subtitle">Select your health goals (choose all that apply)</p>
                {error && <div className="error-message">{error}</div>}
                <div className="dietary-goals-grid">
                    {dietaryGoals.map((goal) => (
                        <DietaryGoalCard
                            key={goal.id}
                            goal={goal.goal}
                            description={goal.description}
                            icon={goal.icon}
                            isSelected={selectedGoals.includes(goal.goal)}
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