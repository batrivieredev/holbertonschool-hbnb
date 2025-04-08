// Attend que le DOM soit chargé
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
});

// Vérifie si l'utilisateur est connecté
async function checkAuth() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = '/login.html';
        return;
    }
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
        // Crée l'objet avec les données du formulaire
        const formData = {
            title: document.getElementById('title').value,
            description: document.getElementById('description').value,
            latitude: parseFloat(document.getElementById('latitude').value),
            longitude: parseFloat(document.getElementById('longitude').value),
            price: parseInt(document.getElementById('price').value)
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
