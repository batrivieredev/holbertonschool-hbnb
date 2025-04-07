document.addEventListener('DOMContentLoaded', () => {
    const placesList = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');

    let places = [];

    // Check authentication and update UI
    function checkAuth() {
        const token = getCookie('token');
        if (token) {
            loginLink.style.display = 'none';
            logoutButton.style.display = 'block';
        } else {
            loginLink.style.display = 'block';
            logoutButton.style.display = 'none';
        }
    }

    // Fetch places from API
    async function fetchPlaces() {
        try {
            const token = getCookie('token');
            const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

            const response = await fetch('http://localhost:5000/api/v1/places', {
                headers: {
                    ...headers,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                places = await response.json();
                filterAndDisplayPlaces();
            } else {
                console.error('Failed to fetch places:', response.statusText);
            }
        } catch (error) {
            console.error('Error fetching places:', error);
        }
    }

    // Filter and display places based on price
    function filterAndDisplayPlaces() {
        const maxPrice = priceFilter.value === 'all' ? Infinity : parseInt(priceFilter.value);
        const filteredPlaces = places.filter(place => maxPrice === Infinity || place.price <= maxPrice);

        placesList.innerHTML = filteredPlaces.map(place => `
            <div class="place-card">
                <div class="place-image-container">
                    <div class="place-image-placeholder">${place.title[0].toUpperCase()}</div>
                </div>
                <div class="place-card-content">
                    <h3 class="place-title">${place.title}</h3>
                    <p class="place-price">$${place.price} per night</p>
                    <a href="place.html?id=${place.id}" class="details-button">View Details</a>
                </div>
            </div>
        `).join('');
    }

    // Handle logout
    function logout() {
        document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        window.location.href = 'login.html';
    }

    // Get cookie helper function
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Event listeners
    priceFilter.addEventListener('change', filterAndDisplayPlaces);
    logoutButton.addEventListener('click', logout);

    // Initialize
    checkAuth();
    fetchPlaces();
});
