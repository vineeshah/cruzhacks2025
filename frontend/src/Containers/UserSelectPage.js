import React from 'react';
import Logo from '../Components/logo'; 
import OptionCard from '../Components/option-card';

const UserSelectPage = () => {

    return (
        <div className='user-select-page'>
            <Logo />
            <div className='user-select-options'>
                <OptionCard
                title='I want takeout'
                imageSrc="https://via.placeholder.com/150" 
                targetPath="/takeout-help" 
                />
                <OptionCard
                title='I want to cook'
                imageSrc="https://via.placeholder.com/150" 
                targetPath="/cooking-help" 
                />
                <OptionCard
                title='Health Advice (AI)'
                imageSrc="https://via.placeholder.com/150" 
                targetPath="/health-advice" 
                />
            </div>
        </div>
    );
};

export default UserSelectPage;