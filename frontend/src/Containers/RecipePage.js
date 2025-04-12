import React from 'react';
import Logo from '../Components/logo';
import RecipePopUp from '../Components/RecipePopUp';

const RecipePage = () => {
    const recipes = [
        {
            recipeName: 'Grilled Chicken Salad',
            cuisine: 'American',
            imageSrc: '/images/grilled-chicken-salad.jpg',
            rating: 4.5,
            goalsMet: 'Low Carb, High Protein',
            source: 'https://example.com/grilled-chicken-salad',
        }
    ];

    return (
        <div className="recipe-page">
        <Logo />
        <h1 className='select-header'>Healthify Recipes</h1>
        <p>Based on your goals we suggest:</p>
        <div className="recipe-list">
            {recipes.map((recipe, index) => (
                    <RecipePopUp
                        key={index}
                        recipeName={recipe.name}
                        cuisine={recipe.cuisine}
                        imageSrc={recipe.imageSrc}
                        rating={recipe.rating}
                        source={recipe.price}
                        goalsMet={recipe.goalsMet}
                    />
            ))}

            </div>
        </div>
    );
};

export default RecipePage;