// Attend que le DOM soit chargé
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

// Vérifie si l'utilisateur est connecté
function checkAuth() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const createPlaceLink = document.getElementById('create-place-link');
    const logoutButton = document.getElementById('logout-button');
    const reviewForm = document.getElementById('review-form');
    const bookingSection = document.getElementById('booking-section');

    if (token) {
        if (loginLink) loginLink.style.display = 'none';
        if (createPlaceLink) createPlaceLink.style.display = 'block';
        if (logoutButton) {
            logoutButton.style.display = 'block';
            logoutButton.addEventListener('click', logout);
        }
        if (reviewForm || bookingSection) {
            fetch('/api/v1/auth/profile', {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            .then(response => response.json())
            .then(data => {
                const urlParams = new URLSearchParams(window.location.search);
                const placeId = urlParams.get('id');
                loadPlace(placeId, data.id, reviewForm, bookingSection);
            });
        }
    } else {
        if (loginLink) loginLink.style.display = 'block';
        if (createPlaceLink) createPlaceLink.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'none';
        if (reviewForm) reviewForm.style.display = 'none';
        if (bookingSection) bookingSection.style.display = 'none';
    }
}

async function loadPlace(placeId, userId, reviewForm, bookingSection) {
    try {
        const response = await fetch(`/api/v1/places/${placeId}`);
        const place = await response.json();

        // Si c'est le propriétaire
        if (place.owner.id === userId) {
            if (reviewForm) reviewForm.style.display = 'none';
            if (bookingSection) bookingSection.style.display = 'none';
            loadBookings(placeId); // Charge les réservations pour le propriétaire
        } else {
            if (reviewForm) reviewForm.style.display = 'block';
            if (bookingSection) bookingSection.style.display = 'block';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Retourne l'icône correspondant à l'équipement
function getAmenityIcon(name) {
    const icons = {
        'WiFi': '📶',
        'Climatisation': '❄️',
        'Chauffage': '🔥',
        'Cuisine': '🍳',
        'TV': '📺',
        'Parking gratuit': '🅿️',
        'Lave-linge': '🧺',
        'Piscine': '🏊‍♂️',
        'Jacuzzi': '🌊',
        'Salle de sport': '🏋️‍♂️'
    };
    return icons[name] || '✨';
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

        // Gestion des photos
        const photosHtml = place.photos && place.photos.length > 0
            ? `
                <div class="place-images-grid">
                    <div class="place-image-main">
                        <img src="${sanitizeHTML(place.photos[0].photo_url)}" alt="Photo principale" class="gallery-img">
                    </div>
                    ${place.photos.slice(1).map(photo => `
                        <div class="place-image-item">
                            <img src="${sanitizeHTML(photo.photo_url)}" alt="${sanitizeHTML(photo.caption || '')}" class="gallery-img">
                        </div>
                    `).join('')}
                </div>
            `
            : `
                <div class="place-image-container">
                    <div class="place-image-placeholder">🏠</div>
                </div>
            `;

        placeDetails.innerHTML = `
            ${photosHtml}
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
                                <li>
                                    <span class="amenity-icon">${getAmenityIcon(amenity.name)}</span>
                                    ${sanitizeHTML(amenity.name)}
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        `;

        // Initialise le formulaire de réservation
        initBookingForm(placeId);

    } catch (error) {
        console.error('Error loading place details:', error);
        showError('Failed to load place details');
    }
}

// Initialise le formulaire de réservation
function initBookingForm(placeId) {
    const form = document.getElementById('booking-form');
    if (!form) return;

    // Date minimum = aujourd'hui
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('start_date').min = today;
    document.getElementById('end_date').min = today;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const token = getCookie('token');
        if (!token) {
            window.location.href = '/login.html';
            return;
        }

        const button = form.querySelector('button[type="submit"]');
        const spinner = button.querySelector('.loading-spinner');
        button.disabled = true;
        spinner.style.display = 'inline-block';

        try {
            const response = await fetch(`/api/v1/places/${placeId}/bookings`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    start_date: document.getElementById('start_date').value,
                    end_date: document.getElementById('end_date').value,
                    message: document.getElementById('message').value
                })
            });

            const result = await response.json();

            if (response.ok) {
                form.reset();
                showSuccess('Demande de réservation envoyée avec succès');
            } else {
                showError(result.error || 'Erreur lors de la réservation');
            }
        } catch (error) {
            showError('Erreur lors de la réservation');
        } finally {
            button.disabled = false;
            spinner.style.display = 'none';
        }
    });
}

// Charge les réservations pour le propriétaire
async function loadBookings(placeId) {
    try {
        const bookingsList = document.getElementById('bookings-list');
        const placeBookings = document.getElementById('place-bookings');
        if (!bookingsList || !placeBookings) return;

        const token = getCookie('token');
        const response = await fetch(`/api/v1/places/${placeId}/bookings`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const bookings = await response.json();

        if (bookings.length > 0) {
            placeBookings.style.display = 'block';
            bookingsList.innerHTML = bookings.map(booking => `
                <div class="booking-card">
                    <div class="booking-header">
                        <span class="booking-user">${sanitizeHTML(booking.user.first_name)} ${sanitizeHTML(booking.user.last_name)}</span>
                        <span class="booking-status">${booking.status}</span>
                    </div>
                    <div class="booking-dates">
                        Du ${new Date(booking.start_date).toLocaleDateString('fr-FR')}
                        au ${new Date(booking.end_date).toLocaleDateString('fr-FR')}
                    </div>
                    ${booking.message ? `
                        <div class="booking-message">
                            ${sanitizeHTML(booking.message)}
                        </div>
                    ` : ''}
                    ${booking.status === 'pending' ? `
                        <div class="booking-actions">
                            <button onclick="updateBooking('${booking.id}', 'confirmed')" class="button success">
                                <span class="icon">✅</span> Accepter
                            </button>
                            <button onclick="updateBooking('${booking.id}', 'cancelled')" class="button danger">
                                <span class="icon">❌</span> Refuser
                            </button>
                        </div>
                    ` : ''}
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading bookings:', error);
    }
}

// Met à jour le statut d'une réservation
async function updateBooking(bookingId, status) {
    try {
        const token = getCookie('token');
        const response = await fetch(`/api/v1/bookings/${bookingId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ status })
        });

        if (response.ok) {
            // Recharge les réservations
            const urlParams = new URLSearchParams(window.location.search);
            const placeId = urlParams.get('id');
            loadBookings(placeId);
        } else {
            showError('Erreur lors de la mise à jour de la réservation');
        }
    } catch (error) {
        showError('Erreur lors de la mise à jour de la réservation');
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

// Gestion du formulaire d'avis
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

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.innerHTML = `
        <span class="icon">✅</span>
        ${message}
    `;
    document.querySelector('main').prepend(successDiv);
    setTimeout(() => successDiv.remove(), 5000);
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <span class="icon">⚠️</span>
        ${message}
    `;
    document.querySelector('main').prepend(errorDiv);
    setTimeout(() => errorDiv.remove(), 5000);
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
