export const getNearbyRestaurants = async (lat, lng, radius) => {
    const token = localStorage.getItem('token');
    const response = await fetch(
        `http://localhost:5000/api/restaurants/search?lat=${lat}&lng=${lng}&radius=${radius}`,
        {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        }
    );
    return response.json();
}; 