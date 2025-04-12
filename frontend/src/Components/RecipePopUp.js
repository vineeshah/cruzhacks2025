import React from 'react';
import './RecipePopUp.css'; 

const RecipePopUp = ({ recipe }) => {
    if (!recipe) return null; 
    return (
        <div className="popup-overlay">
            <div className='recipe-info'>
                <h3 className="recipe-name">{recipe.recipeName}</h3>
                <p className="recipe-cuisine">{recipe.cuisine}</p>
                <p className="recipe-rating">{recipe.rating} / 5</p>
                <p className="recipe-goals-met">{recipe.goalsMet}</p>
                <p className="recipe-source">{recipe.source}</p>
            </div>
        </div>
    );
}

export default RecipePopUp;