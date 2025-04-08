document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');

    // Check if user is already logged in
    const token = getCookie('token');
    if (token) {
        window.location.href = 'index.html';
        return;
    }

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        errorMessage.textContent = '';

        try {
            const response = await fetch('http://localhost:5001/api/v1/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                // Store token in cookie
                document.cookie = `token=${data.access_token}; path=/; max-age=3600`;
                // Redirect to admin page if user is admin, otherwise to main page
                if (data.user && data.user.is_admin) {
                    window.location.href = 'admin.html';
                } else {
                    window.location.href = 'index.html';
                }
            } else {
                errorMessage.textContent = data.message || 'Invalid email or password';
            }
        } catch (error) {
            console.error('Login error:', error);
            errorMessage.textContent = 'An error occurred. Please try again later.';
        }
    });

    // Helper function to get cookie value
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
});
