import React from 'react';
import { Routes, Route } from 'react-router-dom'; // Import Routes and Route
import Homepage from './Containers/Homepage'; // Import Homepage component
import SignIn from './Containers/SignIn'; // Import SignIn component
import SignUp from './Containers/SignUp'; // Import SignUp component
import './App.css';

function App() {
  return (
    <div className="App">
    <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/sign-in" element={<SignIn />} />
        <Route path="/sign-up" element={<SignUp />} />
    </Routes>
</div>
  );
}

export default App;
