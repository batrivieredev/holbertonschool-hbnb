// Gestionnaire de connexion
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const button = e.target.querySelector('button[type="submit"]');
    const spinner = button.querySelector('.loading-spinner');

    // Désactive le bouton et affiche le spinner
    button.disabled = true;
    spinner.style.display = 'inline-block';

    try {
        const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: document.getElementById('email').value,
                password: document.getElementById('password').value
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Stocke le token
            document.cookie = `token=${data.token}; path=/`;

            // Redirige vers la page appropriée
            if (data.user.is_admin) {
                window.location.href = '/admin.html';
            } else {
                window.location.href = '/';
            }
        } else {
            showError(data.error || 'Erreur de connexion', 'login-form');
            button.disabled = false;
            spinner.style.display = 'none';
        }
    } catch (error) {
        console.error('Erreur:', error);
        showError('Une erreur est survenue lors de la connexion', 'login-form');
        button.disabled = false;
        spinner.style.display = 'none';
    }
});

// Gestionnaire d'inscription
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const button = e.target.querySelector('button[type="submit"]');
    const spinner = button.querySelector('.loading-spinner');

    // Désactive le bouton et affiche le spinner
    button.disabled = true;
    spinner.style.display = 'inline-block';

    try {
        const formData = {
            email: document.getElementById('reg-email').value,
            password: document.getElementById('reg-password').value,
            first_name: document.getElementById('reg-firstName').value,
            last_name: document.getElementById('reg-lastName').value,
            is_admin: false  // Toujours false pour les nouveaux utilisateurs
        };

        const response = await fetch('/api/v1/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            // Connecte automatiquement l'utilisateur
            document.cookie = `token=${data.token}; path=/`;
            window.location.href = '/';
        } else {
            showError(data.error || 'Erreur lors de l\'inscription', 'register-form');
            button.disabled = false;
            spinner.style.display = 'none';
        }
    } catch (error) {
        console.error('Erreur:', error);
        showError('Une erreur est survenue lors de l\'inscription', 'register-form');
        button.disabled = false;
        spinner.style.display = 'none';
    }
});

// Affiche un message d'erreur
function showError(message, formId) {
    // Supprime les anciennes erreurs
    const oldError = document.querySelector(`#${formId} + .error-message`);
    if (oldError) {
        oldError.remove();
    }

    // Crée et affiche le nouveau message d'erreur
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <span class="icon">⚠️</span>
        ${message}
    `;

    // Insère l'erreur après le formulaire
    const form = document.getElementById(formId);
    form.parentNode.insertBefore(errorDiv, form.nextSibling);

    // Supprime automatiquement l'erreur après 5 secondes
    setTimeout(() => {
        errorDiv.style.opacity = '0';
        setTimeout(() => errorDiv.remove(), 300);
    }, 5000);
}
