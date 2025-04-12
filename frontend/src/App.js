import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Homepage from './Containers/Homepage';
import UserSelectPage from './Containers/UserSelectPage';
import WelcomePage from './Containers/WelcomePage';
import TakeoutPage from './Containers/TakeoutPage';
import RecipePage from './Containers/RecipePage';
import './App.css';

function App() {
    return (
        <div className="App">
            <Routes>
                <Route path="/" element={<Homepage />} />
                <Route path="/welcome" element={<WelcomePage />} />
                <Route path="/user-select" element={<UserSelectPage />} />
                <Route path="/takeout" element={<TakeoutPage />} />
                <Route path="/cooking" element={<RecipePage />} />
            </Routes>
        </div>
    );
}

export default App;
