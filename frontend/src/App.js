import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Homepage from './Containers/Homepage';
import Login from './Containers/Login';
import Register from './Containers/Register';
import WelcomePage from './Containers/WelcomePage';
import UserSelect from './Containers/UserSelectPage';
import Takeout from './Containers/TakeoutPage';
import Navbar from './Components/Navbar';
import './App.css';

function App() {
    return (
        <div className="App">
            <Navbar />
            <div className="content">
                <Routes>
                    <Route path="/" element={<Homepage />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/welcome" element={<WelcomePage />} />
                    <Route path="/user-select" element={<UserSelect />} />
                    <Route path="/takeout" element={<Takeout />} />
                </Routes>
            </div>
        </div>
    );
}

export default App;
