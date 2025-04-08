document.addEventListener('DOMContentLoaded', () => {
    const createPlaceForm = document.getElementById('create-place-form');
    const errorMessage = document.getElementById('error-message');
    const logoutButton = document.getElementById('logout-button');

    // Check authentication and verify token format
    const token = getCookie('token');
    if (!token) {
        console.log('No token found - redirecting to login');
        window.location.href = 'login.html';
        return;
    }

    // Verify token validity by making a test request
    fetch('http://localhost:5001/api/v1/auth/profile', {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    }).catch(error => {
        console.error('Token validation failed:', error);
        window.location.href = 'login.html';
        return;
    });

    // Handle form submission
    createPlaceForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        errorMessage.textContent = '';

        const formData = {
            title: document.getElementById('title').value,
            description: document.getElementById('description').value,
            price: parseFloat(document.getElementById('price').value),
            latitude: parseFloat(document.getElementById('latitude').value),
            longitude: parseFloat(document.getElementById('longitude').value)
        };

        try {
            const response = await fetch('http://localhost:5001/api/v1/places', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                const data = await response.json();
                // Redirect to the place details page
                window.location.href = `place.html?id=${data.id}`;
            } else {
                const errorData = await response.json();
                console.error('Server error:', errorData);
                errorMessage.textContent = errorData.message || 'Failed to create place. Please try again.';
                if (errorData.missing_fields) {
                    errorMessage.textContent += ` Missing fields: ${errorData.missing_fields.join(', ')}`;
                }
            }
        } catch (error) {
            console.error('Error creating place:', error);
            // Check if it's an auth error
            if (error.status === 401) {
                console.log('Authentication error - redirecting to login');
                window.location.href = 'login.html';
                return;
            }
            errorMessage.textContent = 'An error occurred. Please try again later.';
        }
    });

    // Handle logout
    logoutButton.addEventListener('click', () => {
        document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        window.location.href = 'login.html';
    });

    // Helper function to get cookie value
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
});
