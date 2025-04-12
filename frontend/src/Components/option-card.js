import React from 'react';
import PropTypes from 'prop-types';
import { useNavigate } from 'react-router-dom'; 
import './option-card.css'; 

const OptionCard = ({ title, description, imageSrc, targetPath }) => {
    const navigate = useNavigate(); 

    const handleClick = () => {
        navigate(targetPath); 
    };

    return (
        <div className="option-card" onClick={handleClick}>
            {imageSrc && <img src={imageSrc} alt={title} className="option-card-image" />}
            <h3 className="option-card-title">{title}</h3>
            <p className="option-card-description">{description}</p>
        </div>
    );
};

OptionCard.propTypes = {
    title: PropTypes.string.isRequired,
    description: PropTypes.string,
    imageSrc: PropTypes.string, 
    targetPath: PropTypes.string.isRequired, 
};

OptionCard.defaultProps = {
    description: '',
    imageSrc: '', 
};

export default OptionCard;