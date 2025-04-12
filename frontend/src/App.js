import React from 'react';
import { Routes, Route} from 'react-router-dom'; 
import Homepage from './Containers/Homepage'; 
import UserSelectPage from './Containers/UserSelectPage'; 
import UserGoalsPage from './Containers/UserGoalsPage';
import './App.css';

function App() {
  return (
    <div className="App">
    <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="user-goals" element={<UserGoalsPage />} />
        <Route path="/user-select" element={<UserSelectPage />} />
    </Routes>
</div>
  );
}

export default App;
