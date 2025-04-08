// Exécuté au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    checkAdminAuth();
    loadUsers();
    setupUserForm();
});

// Vérifie que l'utilisateur est un admin
async function checkAdminAuth() {
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

        if (!userData.is_admin) {
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Erreur de vérification admin:', error);
        window.location.href = '/login.html';
    }
}

// Configure le formulaire de création d'utilisateur
function setupUserForm() {
    const form = document.getElementById('create-user-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = {
            email: form.email.value,
            password: form.password.value,
            first_name: form.firstName.value,
            last_name: form.lastName.value,
            is_admin: form.isAdmin.checked
        };

        try {
            const response = await fetch('/api/v1/admin/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('token')}`
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok) {
                showMessage('Utilisateur créé avec succès!', 'success');
                form.reset();
                loadUsers();  // Recharge la liste des utilisateurs
            } else {
                showMessage(result.error || 'Erreur lors de la création', 'error');
            }
        } catch (error) {
            console.error('Erreur:', error);
            showMessage('Erreur lors de la création de l\'utilisateur', 'error');
        }
    });
}

// Charge la liste des utilisateurs
async function loadUsers() {
    try {
        const response = await fetch('/api/v1/admin/users', {
            headers: {
                'Authorization': `Bearer ${getCookie('token')}`
            }
        });

        if (!response.ok) {
            throw new Error('Erreur de chargement des utilisateurs');
        }

        const users = await response.json();
        displayUsers(users);
    } catch (error) {
        console.error('Erreur:', error);
        showMessage('Erreur lors du chargement des utilisateurs', 'error');
    }
}

// Affiche la liste des utilisateurs
function displayUsers(users) {
    const usersList = document.getElementById('users-list');
    usersList.innerHTML = users.map(user => `
        <div class="user-card">
            <div class="user-info">
                <h3>${sanitizeHTML(user.first_name)} ${sanitizeHTML(user.last_name)}</h3>
                <p>${sanitizeHTML(user.email)}</p>
                <p class="user-role">${user.is_admin ? 'Administrateur' : 'Utilisateur'}</p>
            </div>
            <div class="user-actions">
                ${user.is_admin ?
                    `<button onclick="demoteUser('${user.id}')" class="button warning">
                        <span class="icon">⬇️</span> Rétrograder
                    </button>` :
                    `<button onclick="promoteUser('${user.id}')" class="button success">
                        <span class="icon">⬆️</span> Promouvoir
                    </button>`
                }
                <button onclick="deleteUser('${user.id}')" class="button danger">
                    <span class="icon">🗑️</span> Supprimer
                </button>
            </div>
        </div>
    `).join('');
}

// Promeut un utilisateur en admin
async function promoteUser(userId) {
    if (!confirm('Voulez-vous vraiment promouvoir cet utilisateur en administrateur?')) {
        return;
    }

    try {
        const response = await fetch(`/api/v1/admin/users/${userId}/promote`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getCookie('token')}`
            }
        });

        if (response.ok) {
            showMessage('Utilisateur promu avec succès', 'success');
            loadUsers();
        } else {
            const data = await response.json();
            showMessage(data.error || 'Erreur lors de la promotion', 'error');
        }
    } catch (error) {
        console.error('Erreur:', error);
        showMessage('Erreur lors de la promotion de l\'utilisateur', 'error');
    }
}

// Rétrograde un admin en utilisateur normal
async function demoteUser(userId) {
    if (!confirm('Voulez-vous vraiment rétrograder cet administrateur?')) {
        return;
    }

    try {
        const response = await fetch(`/api/v1/admin/users/${userId}/demote`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getCookie('token')}`
            }
        });

        if (response.ok) {
            showMessage('Utilisateur rétrogradé avec succès', 'success');
            loadUsers();
        } else {
            const data = await response.json();
            showMessage(data.error || 'Erreur lors de la rétrogradation', 'error');
        }
    } catch (error) {
        console.error('Erreur:', error);
        showMessage('Erreur lors de la rétrogradation de l\'utilisateur', 'error');
    }
}

// Supprime un utilisateur
async function deleteUser(userId) {
    if (!confirm('Voulez-vous vraiment supprimer cet utilisateur?')) {
        return;
    }

    try {
        const response = await fetch(`/api/v1/admin/users/${userId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${getCookie('token')}`
            }
        });

        if (response.ok) {
            showMessage('Utilisateur supprimé avec succès', 'success');
            loadUsers();
        } else {
            const data = await response.json();
            showMessage(data.error || 'Erreur lors de la suppression', 'error');
        }
    } catch (error) {
        console.error('Erreur:', error);
        showMessage('Erreur lors de la suppression de l\'utilisateur', 'error');
    }
}

// Affiche un message de notification
function showMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    document.querySelector('main').prepend(messageDiv);

    setTimeout(() => messageDiv.remove(), 5000);
}

// Récupère un cookie par son nom
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
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

// Déconnexion de l'utilisateur
function logout() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = '/login.html';
}
