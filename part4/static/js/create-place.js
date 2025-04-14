// Attend que le DOM soit chargé
document.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    await loadAmenities();
    initPhotoManagement();
});

// Vérifie si l'utilisateur est connecté
async function checkAuth() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = '/login.html';
        return;
    }

    try {
        const response = await fetch('/api/v1/auth/profile', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const userData = await response.json();

        // Afficher le nom de l'utilisateur
        const userName = document.getElementById('user-name');
        if (userName) {
            userName.style.display = 'inline-flex';
            userName.querySelector('.name-text').textContent =
                `${userData.first_name} ${userData.last_name}`;
        }
    } catch (error) {
        console.error('Error:', error);
        window.location.href = '/login.html';
    }
}

// Charge la liste des équipements disponibles
async function loadAmenities() {
    try {
        const response = await fetch('/api/v1/amenities');
        const amenities = await response.json();

        const amenitiesList = document.getElementById('amenities-list');
        // Vide la liste existante
        amenitiesList.innerHTML = '';

        // Crée les cases à cocher pour chaque équipement
        amenities.forEach(amenity => {
            const amenityIcon = getAmenityIcon(amenity.name);
            const label = document.createElement('label');
            label.className = 'amenity-item';
            label.innerHTML = `
                <input type="checkbox" name="amenities" value="${amenity.id}">
                <span class="amenity-icon">${amenityIcon}</span> ${amenity.name}
            `;
            amenitiesList.appendChild(label);
        });
    } catch (error) {
        console.error('Erreur lors du chargement des équipements:', error);
        showError('Erreur lors du chargement des équipements');
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

// Initialise la gestion des photos
function initPhotoManagement() {
    const addPhotoButton = document.getElementById('add-photo');
    addPhotoButton.addEventListener('click', addPhotoField);

    // Ajoute les gestionnaires d'événements pour les boutons de suppression existants
    document.querySelectorAll('.remove-photo').forEach(button => {
        button.addEventListener('click', () => removePhotoField(button));
    });
}

// Ajoute un nouveau champ de photo
function addPhotoField() {
    const photosContainer = document.querySelector('.photos-container');
    const photoDiv = document.createElement('div');
    photoDiv.className = 'photo-upload';

    const isFirstPhoto = document.querySelectorAll('.photo-upload').length === 0;

    photoDiv.innerHTML = `
        <input type="text" placeholder="URL de la photo" class="photo-url">
        <input type="text" placeholder="Légende (optionnel)" class="photo-caption">
        <label class="primary-photo">
            <input type="radio" name="primary-photo" ${isFirstPhoto ? 'checked' : ''}>
            Photo principale
        </label>
        <button type="button" class="remove-photo">🗑️</button>
    `;

    // Insère avant le bouton d'ajout
    photosContainer.insertBefore(photoDiv, document.getElementById('add-photo'));

    // Ajoute le gestionnaire d'événement pour le bouton de suppression
    const removeButton = photoDiv.querySelector('.remove-photo');
    removeButton.addEventListener('click', () => removePhotoField(removeButton));
}

// Supprime un champ de photo
function removePhotoField(button) {
    const photoDiv = button.closest('.photo-upload');
    const wasChecked = photoDiv.querySelector('input[type="radio"]').checked;

    photoDiv.remove();

    // Si c'était la photo principale et qu'il reste des photos, sélectionne la première
    if (wasChecked) {
        const firstRadio = document.querySelector('input[type="radio"][name="primary-photo"]');
        if (firstRadio) {
            firstRadio.checked = true;
        }
    }
}

// Récupère les photos du formulaire
function getPhotos() {
    const photos = [];
    document.querySelectorAll('.photo-upload').forEach(photoDiv => {
        const url = photoDiv.querySelector('.photo-url').value.trim();
        if (url) {
            photos.push({
                photo_url: url,
                caption: photoDiv.querySelector('.photo-caption').value.trim(),
                is_primary: photoDiv.querySelector('input[type="radio"]').checked
            });
        }
    });
    return photos;
}

// Récupère les équipements sélectionnés
function getSelectedAmenities() {
    const amenities = [];
    document.querySelectorAll('input[name="amenities"]:checked').forEach(checkbox => {
        amenities.push(checkbox.value);
    });
    return amenities;
}

// Gestion du formulaire de création
document.getElementById('create-place-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const button = e.target.querySelector('button[type="submit"]');
    const spinner = button.querySelector('.loading-spinner');

    // Désactive le bouton et affiche le spinner
    button.disabled = true;
    spinner.style.display = 'inline-block';

    try {
        // Vérifie si au moins une photo est fournie
        const photos = getPhotos();
        const amenities = getSelectedAmenities();
        const latitude = parseFloat(document.getElementById('latitude').value);
        const longitude = parseFloat(document.getElementById('longitude').value);

        // Récupère l'adresse à partir des coordonnées
        const locationResponse = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`);
        const locationData = await locationResponse.json();
        const location = locationData.display_name || 'Adresse non trouvée';

        // Crée l'objet avec les données du formulaire
        const formData = {
            title: document.getElementById('title').value,
            description: document.getElementById('description').value,
            latitude: latitude,
            longitude: longitude,
            location: location,
            price: parseInt(document.getElementById('price').value),
            amenities: amenities,
            photos: photos
        };

        // Validation des coordonnées
        if (formData.latitude < -90 || formData.latitude > 90) {
            throw new Error('La latitude doit être entre -90 et 90 degrés');
        }
        if (formData.longitude < -180 || formData.longitude > 180) {
            throw new Error('La longitude doit être entre -180 et 180 degrés');
        }

        // Envoie la requête
        const response = await fetch('/api/v1/places', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getCookie('token')}`
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (response.ok) {
            // Redirige vers la page du lieu créé
            window.location.href = `/place.html?id=${result.id}`;
        } else {
            showError(result.error || 'Erreur lors de la création du lieu');
            button.disabled = false;
            spinner.style.display = 'none';
        }
    } catch (error) {
        console.error('Erreur:', error);
        showError(error.message || 'Une erreur est survenue');
        button.disabled = false;
        spinner.style.display = 'none';
    }
});

// Affiche un message d'erreur
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <span class="icon">⚠️</span>
        ${message}
    `;

    const form = document.getElementById('create-place-form');
    const existingError = form.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    form.parentNode.insertBefore(errorDiv, form);

    setTimeout(() => {
        errorDiv.style.opacity = '0';
        setTimeout(() => errorDiv.remove(), 300);
    }, 5000);
}

// Récupère un cookie par son nom
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}
