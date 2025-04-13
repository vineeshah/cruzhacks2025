import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Homepage from './Containers/Homepage';
import Login from './Containers/Login';
import Register from './Containers/Register';
import WelcomePage from './Containers/WelcomePage';
import UserSelect from './Containers/UserSelectPage';
import Takeout from './Containers/TakeoutPage';
import Navbar from './Components/Navbar';
import RestaurantDetails from './Containers/RestaurantDetails';
// import PrivateRoute from './Components/PrivateRoute';
import './App.css';

function App() {
    return (
        <div className="App">
            <div className="content">
                <Routes>
                    <Route path="/" element={<Homepage />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/welcome" element={<WelcomePage />} />
                    <Route path="/user-select" element={<UserSelect />} />
                    <Route path="/takeout" element={<Takeout />} />
                    <Route path="/restaurants/:placeId" element={<RestaurantDetails />} />
                </Routes>
            </div>
        </div>
    );
}

export default App;
