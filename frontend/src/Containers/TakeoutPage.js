import React from 'react';
import './TakeoutPage.css';
import Logo from '../Components/logo';
import RestaurantPopUp from '../Components/RestaurantPopUp';

const TakeoutPage = () => {
    const restaurants = [
        {
            name: 'Healthy Bites',
            cuisine: 'Organic',
            imageSrc: '/images/healthy-bites.jpg',
            rating: 4.5,
            price: '$$',
            goalsMet: 'Low Carb, High Protein',
        },
        {
            name: 'Green Eats',
            cuisine: 'Plant-Based',
            imageSrc: '/images/green-eats.jpg',
            rating: 4.7,
            price: '$$',
            goalsMet: 'Vegan, Gluten-Free',
        },
        {
            name: 'Protein Palace',
            cuisine: 'Fitness Meals',
            imageSrc: '/images/protein-palace.jpg',
            rating: 4.8,
            price: '$$$',
            goalsMet: 'High Protein',
        },
        {
            name: 'Keto Kitchen',
            cuisine: 'Keto-Friendly',
            imageSrc: '/images/keto-kitchen.jpg',
            rating: 4.6,
            price: '$$$',
            goalsMet: 'Low Carb, Keto',
        },
        {
            name: 'Vegan Vibes',
            cuisine: 'Vegan',
            imageSrc: '/images/vegan-vibes.jpg',
            rating: 4.9,
            price: '$$',
            goalsMet: 'Vegan',
        },
        {
            name: 'Gluten-Free Goodness',
            cuisine: 'Gluten-Free',
            imageSrc: '/images/gluten-free-goodness.jpg',
            rating: 4.4,
            price: '$$',
            goalsMet: 'Gluten-Free',
        },
        {
            name: 'Low Carb Cafe',
            cuisine: 'Low Carb',
            imageSrc: '/images/low-carb-cafe.jpg',
            rating: 4.3,
            price: '$',
            goalsMet: 'Low Carb',
        },
        {
            name: 'Balanced Bites',
            cuisine: 'Balanced Meals',
            imageSrc: '/images/balanced-bites.jpg',
            rating: 4.5,
            price: '$$',
            goalsMet: 'Balanced Diet',
        },
    ];

    return (
        <div className="takeout-page">
            <Logo />
            <h1 className='select-header'>Healthify Takeout</h1>
            <p>Based on your goals we suggest:</p>
            <div className="restaurant-list">
                {restaurants.map((restaurant, index) => (
                    <RestaurantPopUp
                        key={index}
                        name={restaurant.name}
                        cuisine={restaurant.cuisine}
                        imageSrc={restaurant.imageSrc}
                        rating={restaurant.rating}
                        price={restaurant.price}
                        goalsMet={restaurant.goalsMet}
                    />
                ))}
            </div>
        </div>
    );
};

export default TakeoutPage;