// Attend que le DOM soit chargé
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    loadPlaces();
});

// Vérifie si l'utilisateur est connecté
function checkAuth() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const createPlaceLink = document.getElementById('create-place-link');
    const logoutButton = document.getElementById('logout-button');

    if (token) {
        if (loginLink) loginLink.style.display = 'none';
        if (createPlaceLink) createPlaceLink.style.display = 'block';
        if (logoutButton) {
            logoutButton.style.display = 'block';
            logoutButton.addEventListener('click', logout);
        }

        // Vérifie si l'utilisateur est admin
        fetch('/api/v1/auth/profile', {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        .then(response => response.json())
        .then(data => {
            if (data.is_admin) {
                document.getElementById('admin-link').style.display = 'block';
            }
        });
    } else {
        if (loginLink) loginLink.style.display = 'block';
        if (createPlaceLink) createPlaceLink.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'none';
    }
}

// Charge la liste des lieux
async function loadPlaces(maxPrice = null) {
    try {
        const url = maxPrice ? `/api/v1/places?max_price=${maxPrice}` : '/api/v1/places';
        const response = await fetch(url);
        const places = await response.json();

        const placesContainer = document.getElementById('places-list');

        if (places.length === 0) {
            placesContainer.innerHTML = `
                <div class="no-places">
                    <p>Aucun lieu disponible</p>
                </div>
            `;
            return;
        }

        placesContainer.innerHTML = places.map(place => `
            <div class="place-card" onclick="window.location.href='/place.html?id=${place.id}'">
                ${renderPlacePhoto(place)}
                <div class="place-card-content">
                    <h3>${sanitizeHTML(place.title)}</h3>
                    <p class="place-location">
                        <span class="icon">📍</span>
                        Lat: ${place.latitude}, Long: ${place.longitude}
                    </p>
                    <p class="place-price">
                        ${new Intl.NumberFormat('fr-FR', {
                            style: 'currency',
                            currency: 'EUR'
                        }).format(place.price)} / nuit
                    </p>
                    ${renderAmenities(place.amenities)}
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Error loading places:', error);
        showError('Failed to load places');
    }
}

// Affiche la photo principale d'un lieu ou un placeholder
function renderPlacePhoto(place) {
    if (place.photos && place.photos.length > 0) {
        const primaryPhoto = place.photos.find(photo => photo.is_primary) || place.photos[0];
        return `
            <div class="place-card-image">
                <img src="${sanitizeHTML(primaryPhoto.photo_url)}"
                     alt="${sanitizeHTML(primaryPhoto.caption || place.title)}"
                     onerror="this.onerror=null; this.src='data:image/svg+xml,<svg xmlns=\\'http://www.w3.org/2000/svg\\' viewBox=\\'0 0 100 100\\'><text y=\\'.9em\\' font-size=\\'90\\'>🏠</text></svg>'">
            </div>
        `;
    }
    return `
        <div class="place-card-image placeholder">
            <span class="placeholder-icon">🏠</span>
        </div>
    `;
}

// Affiche les équipements d'un lieu
function renderAmenities(amenities) {
    if (!amenities || amenities.length === 0) return '';

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

    return `
        <div class="place-amenities">
            ${amenities.slice(0, 4).map(amenity => `
                <span class="amenity-tag" title="${sanitizeHTML(amenity.name)}">
                    ${icons[amenity.name] || '✨'}
                </span>
            `).join('')}
            ${amenities.length > 4 ? `
                <span class="amenity-tag more" title="${amenities.slice(4).map(a => a.name).join(', ')}">
                    +${amenities.length - 4}
                </span>
            ` : ''}
        </div>
    `;
}

// Filtre par prix
document.getElementById('price-filter')?.addEventListener('input', (e) => {
    const maxPrice = e.target.value;
    document.getElementById('price-value').textContent = `${maxPrice}€`;
    loadPlaces(maxPrice);
});

// Affiche une erreur
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

// Sanitize HTML
function sanitizeHTML(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// Récupère un cookie par son nom
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Déconnexion
function logout() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = '/login.html';
}
