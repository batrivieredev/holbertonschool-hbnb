document.addEventListener('DOMContentLoaded', () => {
    const createUserForm = document.getElementById('create-user-form');
    const usersList = document.getElementById('users-list');
    const errorMessage = document.getElementById('error-message');
    const logoutButton = document.getElementById('logout-button');

    // Check if user is admin
    async function checkAdmin() {
        const token = getCookie('token');
        if (!token) {
            window.location.href = 'login.html';
            return;
        }

        try {
            const response = await fetch('http://localhost:5001/api/v1/auth/profile', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const userData = await response.json();
                if (!userData.is_admin) {
                    window.location.href = 'index.html';
                }
            } else {
                window.location.href = 'login.html';
            }
        } catch (error) {
            console.error('Error checking admin status:', error);
            window.location.href = 'login.html';
        }
    }

    // Fetch all users
    async function fetchUsers() {
        try {
            const token = getCookie('token');
            const response = await fetch('http://localhost:5001/api/v1/admin/users', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const users = await response.json();
                displayUsers(users);
            } else {
                console.error('Failed to fetch users:', response.statusText);
            }
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    }

    // Display users in the list
    function displayUsers(users) {
        usersList.innerHTML = users.map(user => `
            <div class="user-card">
                <div class="user-info">
                    <h3>${user.first_name} ${user.last_name}</h3>
                    <p>Email: ${user.email}</p>
                    <p>Role: ${user.is_admin ? 'Admin' : 'User'}</p>
                </div>
                <button class="delete-user-btn" data-id="${user.id}">Delete</button>
            </div>
        `).join('');

        // Add event listeners to delete buttons
        document.querySelectorAll('.delete-user-btn').forEach(button => {
            button.addEventListener('click', () => deleteUser(button.dataset.id));
        });
    }

    // Create new user
    async function createUser(userData) {
        try {
            const token = getCookie('token');
            const response = await fetch('http://localhost:5001/api/v1/admin/users', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();

            if (response.ok) {
                createUserForm.reset();
                errorMessage.textContent = '';
                fetchUsers();  // Refresh the users list
            } else {
                errorMessage.textContent = data.message || 'Failed to create user';
            }
        } catch (error) {
            console.error('Error creating user:', error);
            errorMessage.textContent = 'An error occurred while creating the user';
        }
    }

    // Delete user
    async function deleteUser(userId) {
        if (!confirm('Are you sure you want to delete this user?')) {
            return;
        }

        try {
            const token = getCookie('token');
            const response = await fetch(`http://localhost:5001/api/v1/admin/users/${userId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                fetchUsers();  // Refresh the users list
            } else {
                const error = await response.json();
                alert(error.message || 'Failed to delete user');
            }
        } catch (error) {
            console.error('Error deleting user:', error);
            alert('An error occurred while deleting the user');
        }
    }

    // Handle form submission
    createUserForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const userData = {
            first_name: document.getElementById('first-name').value,
            last_name: document.getElementById('last-name').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            is_admin: document.getElementById('is-admin').checked
        };
        createUser(userData);
    });

    // Handle logout
    logoutButton.addEventListener('click', () => {
        document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        window.location.href = 'login.html';
    });

    // Get cookie helper function
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Initialize
    checkAdmin();
    fetchUsers();
});
