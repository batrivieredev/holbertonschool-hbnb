document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    if (placeId) {
        loadPlaceDetails(placeId);
        loadReviews(placeId);
    } else {
        window.location.href = '/';
    }
});

function checkAuth() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const createPlaceLink = document.getElementById('create-place-link');
    const logoutButton = document.getElementById('logout-button');
    const reviewForm = document.getElementById('review-form');

    if (token) {
        if (loginLink) loginLink.style.display = 'none';
        if (createPlaceLink) createPlaceLink.style.display = 'block';
        if (logoutButton) {
            logoutButton.style.display = 'block';
            logoutButton.addEventListener('click', logout);
        }
        if (reviewForm) {
            fetch('/api/v1/auth/profile', {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            .then(response => response.json())
            .then(data => {
                const urlParams = new URLSearchParams(window.location.search);
                const placeId = urlParams.get('id');
                // Don't show review form if user is the owner
                loadPlace(placeId, data.id, reviewForm);
            });
        }
    } else {
        if (loginLink) loginLink.style.display = 'block';
        if (createPlaceLink) createPlaceLink.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'none';
        if (reviewForm) reviewForm.style.display = 'none';
    }
}

async function loadPlace(placeId, userId, reviewForm) {
    try {
        const response = await fetch(`/api/v1/places/${placeId}`);
        const place = await response.json();
        if (place.owner.id !== userId) {
            reviewForm.style.display = 'block';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function loadPlaceDetails(placeId) {
    try {
        const response = await fetch(`/api/v1/places/${placeId}`);
        const place = await response.json();

        const placeDetails = document.getElementById('place-details');
        const priceFormatted = new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: 'EUR'
        }).format(place.price);

        placeDetails.innerHTML = `
            <div class="place-image-container">
                <div class="place-image-placeholder">🏠</div>
            </div>
            <div class="place-content">
                <h1>${sanitizeHTML(place.title)}</h1>
                <p class="place-location">
                    <span class="icon">📍</span>
                    Latitude: ${place.latitude}, Longitude: ${place.longitude}
                </p>
                <p class="place-price">${priceFormatted} / nuit</p>
                <div class="place-description">
                    ${sanitizeHTML(place.description || 'Aucune description disponible.')}
                </div>
                <div class="place-owner">
                    <p><strong>Propriétaire:</strong> ${sanitizeHTML(place.owner.first_name)} ${sanitizeHTML(place.owner.last_name)}</p>
                </div>
                ${place.amenities && place.amenities.length > 0 ? `
                    <div class="place-amenities">
                        <h3>Équipements</h3>
                        <ul>
                            ${place.amenities.map(amenity => `
                                <li>${sanitizeHTML(amenity.name)}</li>
                            `).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        `;
    } catch (error) {
        console.error('Error loading place details:', error);
        showError('Failed to load place details');
    }
}

async function loadReviews(placeId) {
    try {
        const response = await fetch(`/api/v1/places/${placeId}/reviews`);
        const reviews = await response.json();

        const reviewsList = document.getElementById('reviews-list');
        if (reviews.length === 0) {
            reviewsList.innerHTML = '<p>Aucun avis pour le moment.</p>';
            return;
        }

        reviewsList.innerHTML = reviews.map(review => `
            <div class="review-card">
                <div class="review-header">
                    <span class="review-author">${sanitizeHTML(review.user.first_name)} ${sanitizeHTML(review.user.last_name)}</span>
                    <span class="review-rating">
                        ${'⭐'.repeat(review.rating)}
                    </span>
                </div>
                <p class="review-text">${sanitizeHTML(review.text)}</p>
                <div class="review-date">
                    ${new Date(review.created_at).toLocaleDateString('fr-FR')}
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Error loading reviews:', error);
        showError('Failed to load reviews');
    }
}

document.getElementById('add-review-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const token = getCookie('token');
    if (!token) {
        window.location.href = '/login.html';
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    const rating = document.getElementById('rating').value;
    const text = document.getElementById('text').value;

    try {
        const response = await fetch(`/api/v1/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ rating: parseInt(rating), text })
        });

        if (response.ok) {
            document.getElementById('rating').value = '';
            document.getElementById('text').value = '';
            loadReviews(placeId);
        } else {
            const data = await response.json();
            showError(data.error || 'Failed to submit review');
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        showError('Failed to submit review');
    }
});

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.querySelector('main').prepend(errorDiv);

    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

function sanitizeHTML(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function logout() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = '/login.html';
}
