document.addEventListener('DOMContentLoaded', () => {
    const placeInfo = document.getElementById('place-info');
    const reviewsList = document.getElementById('reviews-list');
    const addReviewSection = document.getElementById('add-review-section');
    const reviewForm = document.getElementById('review-form');
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');

    // Get place ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    // Check authentication and update UI
    function checkAuth() {
        const token = getCookie('token');
        if (token) {
            loginLink.style.display = 'none';
            logoutButton.style.display = 'block';
            addReviewSection.style.display = 'block';
        } else {
            loginLink.style.display = 'block';
            logoutButton.style.display = 'none';
            addReviewSection.style.display = 'none';
        }
    }

    // Fetch place details
    async function fetchPlaceDetails() {
        try {
            const token = getCookie('token');
            const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

            const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
                headers: {
                    ...headers,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const place = await response.json();
                displayPlaceDetails(place);
                fetchReviews();
            } else {
                console.error('Failed to fetch place details:', response.statusText);
                window.location.href = 'index.html';
            }
        } catch (error) {
            console.error('Error fetching place details:', error);
        }
    }

    // Display place details
    function displayPlaceDetails(place) {
        placeInfo.innerHTML = `
            <h1>${place.title}</h1>
            <div class="place-image-container">
                <div class="place-image-placeholder">${place.title[0].toUpperCase()}</div>
            </div>
            <div class="place-info">
                <p class="place-price">$${place.price} per night</p>
                <p class="place-description">${place.description || 'No description available'}</p>
                <p class="place-location">Location: ${place.latitude}, ${place.longitude}</p>
            </div>
        `;
    }

    // Fetch reviews
    async function fetchReviews() {
        try {
            const token = getCookie('token');
            const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

            const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, {
                headers: {
                    ...headers,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const reviews = await response.json();
                displayReviews(reviews);
            } else {
                console.error('Failed to fetch reviews:', response.statusText);
            }
        } catch (error) {
            console.error('Error fetching reviews:', error);
        }
    }

    // Display reviews
    function displayReviews(reviews) {
        if (reviews.length === 0) {
            reviewsList.innerHTML = '<p>No reviews yet. Be the first to review!</p>';
            return;
        }

        reviewsList.innerHTML = reviews.map(review => `
            <div class="review-card">
                <div class="review-header">
                    <span class="review-rating">Rating: ${review.rating}/5</span>
                    <span class="review-date">${new Date(review.created_at).toLocaleDateString()}</span>
                </div>
                <p class="review-text">${review.text}</p>
            </div>
        `).join('');
    }

    // Submit review
    async function submitReview(text, rating) {
        try {
            const token = getCookie('token');
            if (!token) {
                window.location.href = 'login.html';
                return;
            }

            const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text, rating: parseInt(rating) })
            });

            if (response.ok) {
                reviewForm.reset();
                fetchReviews();
            } else {
                const error = await response.json();
                alert(error.message || 'Failed to submit review');
            }
        } catch (error) {
            console.error('Error submitting review:', error);
            alert('An error occurred while submitting the review');
        }
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
    reviewForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const text = document.getElementById('review-text').value;
        const rating = document.getElementById('rating').value;
        submitReview(text, rating);
    });

    logoutButton.addEventListener('click', logout);

    // Initialize
    checkAuth();
    fetchPlaceDetails();
});
