// Exécuté au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    checkAdminAuth();
    loadUsers();
    setupUserForm();
    setupUserManagement();
});

// Variables globales pour stocker les données des utilisateurs
let usersData = [];

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
                loadUsers();
            } else {
                showMessage(result.error || 'Erreur lors de la création', 'error');
            }
        } catch (error) {
            console.error('Erreur:', error);
            showMessage('Erreur lors de la création de l\'utilisateur', 'error');
        }
    });
}

// Configure la gestion des utilisateurs
function setupUserManagement() {
    const userSelect = document.getElementById('userManageSelect');
    const actionsDiv = document.getElementById('userManageActions');
    const passwordForm = document.getElementById('password-form');
    const adminCheckbox = document.getElementById('selectedUserAdmin');

    // Gestionnaire de changement d'utilisateur
    userSelect.addEventListener('change', () => {
        const userId = userSelect.value;
        if (userId) {
            const selectedUser = usersData.find(user => user.id === userId);
            if (selectedUser) {
                displayUserDetails(selectedUser);
                actionsDiv.style.display = 'block';
            }
        } else {
            actionsDiv.style.display = 'none';
        }
    });

    // Gestionnaire du formulaire de mot de passe
    passwordForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const userId = userSelect.value;
        const newPassword = document.getElementById('newPassword').value;

        if (!userId || !newPassword) {
            showMessage('Veuillez sélectionner un utilisateur et saisir un mot de passe', 'error');
            return;
        }

        await updateUserPassword(userId, newPassword);
    });

    // Gestionnaire du changement de statut admin
    adminCheckbox.addEventListener('change', async () => {
        const userId = userSelect.value;
        if (userId) {
            if (adminCheckbox.checked) {
                await promoteUser(userId);
            } else {
                await demoteUser(userId);
            }
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

        usersData = await response.json();
        updateUserSelect(usersData);
    } catch (error) {
        console.error('Erreur:', error);
        showMessage('Erreur lors du chargement des utilisateurs', 'error');
    }
}

// Met à jour le menu déroulant des utilisateurs
function updateUserSelect(users) {
    const userSelect = document.getElementById('userManageSelect');

    userSelect.innerHTML = `
        <option value="">Choisir un utilisateur</option>
        ${users.map(user => `
            <option value="${user.id}">
                ${sanitizeHTML(user.first_name)} ${sanitizeHTML(user.last_name)} (${sanitizeHTML(user.email)})
            </option>
        `).join('')}
    `;
}

// Affiche les détails de l'utilisateur sélectionné
function displayUserDetails(user) {
    const infoDiv = document.getElementById('selectedUserInfo');
    infoDiv.innerHTML = `
        <p><strong>Nom complet :</strong> ${sanitizeHTML(user.first_name)} ${sanitizeHTML(user.last_name)}</p>
        <p><strong>Email :</strong> ${sanitizeHTML(user.email)}</p>
        <p><strong>Statut :</strong> ${user.is_admin ? 'Administrateur' : 'Utilisateur'}</p>
    `;

    document.getElementById('selectedUserAdmin').checked = user.is_admin;
}

// Met à jour le mot de passe d'un utilisateur
async function updateUserPassword(userId, newPassword) {
    try {
        const response = await fetch(`/api/v1/admin/users/${userId}/password`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getCookie('token')}`
            },
            body: JSON.stringify({ password: newPassword })
        });

        if (response.ok) {
            showMessage('Mot de passe modifié avec succès', 'success');
            document.getElementById('password-form').reset();
        } else {
            const data = await response.json();
            showMessage(data.error || 'Erreur lors de la modification du mot de passe', 'error');
        }
    } catch (error) {
        console.error('Erreur:', error);
        showMessage('Erreur lors de la modification du mot de passe', 'error');
    }
}

// Promeut un utilisateur en admin
async function promoteUser(userId) {
    if (!confirm('Voulez-vous vraiment promouvoir cet utilisateur en administrateur?')) {
        document.getElementById('selectedUserAdmin').checked = false;
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
            document.getElementById('selectedUserAdmin').checked = false;
        }
    } catch (error) {
        console.error('Erreur:', error);
        showMessage('Erreur lors de la promotion de l\'utilisateur', 'error');
        document.getElementById('selectedUserAdmin').checked = false;
    }
}

// Rétrograde un admin en utilisateur normal
async function demoteUser(userId) {
    if (!confirm('Voulez-vous vraiment rétrograder cet administrateur?')) {
        document.getElementById('selectedUserAdmin').checked = true;
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
            document.getElementById('selectedUserAdmin').checked = true;
        }
    } catch (error) {
        console.error('Erreur:', error);
        showMessage('Erreur lors de la rétrogradation de l\'utilisateur', 'error');
        document.getElementById('selectedUserAdmin').checked = true;
    }
}

// Supprime l'utilisateur sélectionné
function deleteSelectedUser() {
    const userId = document.getElementById('userManageSelect').value;
    if (!userId) return;

    if (!confirm('Voulez-vous vraiment supprimer cet utilisateur?')) {
        return;
    }

    deleteUser(userId);
}

// Supprime un utilisateur
async function deleteUser(userId) {
    try {
        const response = await fetch(`/api/v1/admin/users/${userId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${getCookie('token')}`
            }
        });

        if (response.ok) {
            showMessage('Utilisateur supprimé avec succès', 'success');
            document.getElementById('userManageActions').style.display = 'none';
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

// Déconnexion
function logout() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = '/login.html';
}
