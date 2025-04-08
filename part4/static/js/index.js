// Exécuté quand le DOM est chargé
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    loadPlaces();
    setupPriceFilter();
});

// Vérifie l'état de l'authentification et met à jour l'interface
async function checkAuth() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const createPlaceLink = document.getElementById('create-place-link');
    const adminLink = document.getElementById('admin-link');
    const logoutButton = document.getElementById('logout-button');

    if (token) {
        // L'utilisateur est connecté
        loginLink.style.display = 'none';
        createPlaceLink.style.display = 'block';
        logoutButton.style.display = 'block';
        logoutButton.addEventListener('click', logout);

        // Vérifie si l'utilisateur est admin
        try {
            const response = await fetch('/api/v1/auth/profile', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const userData = await response.json();
            if (userData.is_admin) {
                adminLink.style.display = 'block';
            }
        } catch (error) {
            console.error('Erreur lors de la vérification du profil:', error);
        }
    } else {
        // L'utilisateur n'est pas connecté
        loginLink.style.display = 'block';
        createPlaceLink.style.display = 'none';
        adminLink.style.display = 'none';
        logoutButton.style.display = 'none';
    }
}

// Configure le filtre de prix
function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', () => {
            loadPlaces(priceFilter.value);
        });
    }
}

// Charge la liste des lieux avec filtre de prix optionnel
async function loadPlaces(maxPrice = null) {
    try {
        const placesList = document.getElementById('places-list');
        let url = '/api/v1/places';
        if (maxPrice && maxPrice !== 'all') {
            url += `?max_price=${maxPrice}`;
        }

        const response = await fetch(url);
        const places = await response.json();

        if (!Array.isArray(places)) {
            throw new Error('Format de réponse invalide');
        }

        // Vide la liste actuelle
        placesList.innerHTML = '';

        // Ajoute les nouvelles cartes
        places.forEach(place => {
            const placeCard = createPlaceCard(place);
            placesList.appendChild(placeCard);
        });
    } catch (error) {
        console.error('Erreur lors du chargement des lieux:', error);
        showError('Impossible de charger les lieux. Veuillez réessayer plus tard.');
    }
}

// Crée une carte pour un lieu
function createPlaceCard(place) {
    const card = document.createElement('div');
    card.className = 'place-card';

    const priceFormatted = new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(place.price);

    card.innerHTML = `
        <div class="place-image-container">
            <div class="place-image-placeholder">🏠</div>
        </div>
        <div class="place-card-content">
            <h3 class="place-title">${sanitizeHTML(place.title)}</h3>
            <p class="place-price">${priceFormatted} / nuit</p>
            <p class="place-description">${sanitizeHTML(place.description || '')}</p>
            <button class="button" onclick="viewPlaceDetails('${place.id}')">
                <span class="icon">👁️</span> Voir les détails
            </button>
        </div>
    `;
    return card;
}

// Redirige vers la page de détails d'un lieu
function viewPlaceDetails(placeId) {
    window.location.href = `/place.html?id=${placeId}`;
}

// Affiche un message d'erreur
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.querySelector('main').prepend(errorDiv);

    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Nettoie les chaînes de caractères pour l'affichage HTML
function sanitizeHTML(str) {
    if (!str) return '';
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

// Déconnexion de l'utilisateur
function logout() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = '/login.html';
}
