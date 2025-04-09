    // Attend que le DOM soit chargé
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    if (placeId) {
        loadPlaceDetails(placeId);
        loadReviews(placeId);
    } else {
        window.location.href = '/';
    }
});

// Vérifie si l'utilisateur est connecté
function checkAuth() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const createPlaceLink = document.getElementById('create-place-link');
    const logoutButton = document.getElementById('logout-button');
    const reviewForm = document.getElementById('review-form');
    const bookingSection = document.getElementById('booking-section');

    if (token) {
        if (loginLink) loginLink.style.display = 'none';
        if (createPlaceLink) createPlaceLink.style.display = 'block';
        if (logoutButton) {
            logoutButton.style.display = 'block';
            logoutButton.addEventListener('click', logout);
        }
        if (reviewForm || bookingSection) {
            fetch('/api/v1/auth/profile', {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            .then(response => response.json())
            .then(data => {
                const urlParams = new URLSearchParams(window.location.search);
                const placeId = urlParams.get('id');
                loadPlace(placeId, data.id, reviewForm, bookingSection);
            });
        }
    } else {
        if (loginLink) loginLink.style.display = 'block';
        if (createPlaceLink) createPlaceLink.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'none';
        if (reviewForm) reviewForm.style.display = 'none';
        if (bookingSection) bookingSection.style.display = 'none';
    }
}

async function loadPlace(placeId, userId, reviewForm, bookingSection) {
    try {
        const token = getCookie('token');
        // Pour les places, on n'a pas besoin de token car c'est public
        const response = await fetch(`/api/v1/places/${placeId}`);
        const place = await response.json();

        if (!token) {
            // Si pas connecté, on cache les sections interactives
            if (reviewForm) reviewForm.style.display = 'none';
            if (bookingSection) bookingSection.style.display = 'none';
            return;
        }

        // Récupère les réservations avec le token
        const bookingsResponse = await fetch(`/api/v1/places/${placeId}/bookings`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!bookingsResponse.ok) {
            throw new Error('Failed to fetch bookings');
        }

        const bookings = await bookingsResponse.json();

        // Si c'est le propriétaire
        if (place.owner.id === userId) {
            if (reviewForm) reviewForm.style.display = 'none';
            if (bookingSection) bookingSection.style.display = 'none';
            loadBookings(placeId, bookings);
        } else {
            if (reviewForm) reviewForm.style.display = 'block';
            if (bookingSection) {
                bookingSection.style.display = 'block';
                // Initialise le calendrier avec le lieu et les réservations
                initBookingForm(placeId, place, bookings.filter(b => b.status === 'confirmed'));
            }
        }

        // Affiche les périodes réservées pour tous les utilisateurs
        displayBookedPeriods(bookings.filter(b => b.status === 'confirmed'));
    } catch (error) {
        console.error('Error:', error);
        if (error.message === 'Failed to fetch bookings') {
            showError('Erreur lors de la récupération des réservations');
        }
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

// Génère les dates à désactiver dans le calendrier
function generateDisabledDates(bookedPeriods) {
    const disabledDates = [];

    bookedPeriods.forEach(period => {
        if (period.status === 'confirmed') {
            let current = new Date(period.start_date);
            const end = new Date(period.end_date);

            while (current <= end) {
                disabledDates.push(new Date(current));
                current.setDate(current.getDate() + 1);
            }
        }
    });

    return disabledDates;
}

// Vérifie si une plage de dates est disponible
function isDateRangeAvailable(start, end, bookedPeriods) {
    const startDate = new Date(start);
    const endDate = new Date(end);

    return !bookedPeriods.some(period => {
        if (period.status !== 'confirmed') return false;

        const bookedStart = new Date(period.start_date);
        const bookedEnd = new Date(period.end_date);

        return (startDate <= bookedEnd && endDate >= bookedStart);
    });
}

async function loadPlaceDetails(placeId) {
    try {
        const token = getCookie('token');
        let userId = null;

        // Get user profile if logged in
        if (token) {
            try {
                const profileResponse = await fetch('/api/v1/auth/profile', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (profileResponse.ok) {
                    const profile = await profileResponse.json();
                    userId = profile.id;
                }
            } catch (error) {
                console.error('Error fetching profile:', error);
            }
        }

        // Get place details and confirmed bookings
        const [placeResponse, bookingsResponse] = await Promise.all([
            fetch(`/api/v1/places/${placeId}`),
            token ? fetch(`/api/v1/places/${placeId}/bookings`, {
                headers: { 'Authorization': `Bearer ${token}` }
            }) : Promise.resolve(null)
        ]);

        if (!placeResponse.ok) {
            throw new Error('Failed to load place details');
        }

        const place = await placeResponse.json();
        let confirmedBookings = [];

        if (bookingsResponse && bookingsResponse.ok) {
            const bookings = await bookingsResponse.json();
            confirmedBookings = bookings.filter(b => b.status === 'confirmed');
        }

        // Render place details
        const placeDetails = document.getElementById('place-details');
        const priceFormatted = new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: 'EUR'
        }).format(place.price);

        // Gestion des photos
        const photosHtml = place.photos && place.photos.length > 0
            ? `
                <div class="place-images-grid">
                    <div class="place-image-main">
                        <img src="${sanitizeHTML(place.photos[0].photo_url)}" alt="Photo principale" class="gallery-img">
                    </div>
                    ${place.photos.slice(1).map(photo => `
                        <div class="place-image-item">
                            <img src="${sanitizeHTML(photo.photo_url)}" alt="${sanitizeHTML(photo.caption || '')}" class="gallery-img">
                        </div>
                    `).join('')}
                </div>
            `
            : `
                <div class="place-image-container">
                    <div class="place-image-placeholder">🏠</div>
                </div>
            `;

        placeDetails.innerHTML = `
            ${photosHtml}
            <div class="place-content">
                <h1>${sanitizeHTML(place.title)}</h1>
                <p class="place-location">
                    <span class="icon">📍</span>
                    Latitude: ${place.latitude}, Longitude: ${place.longitude}
                </p>
                <p class="place-price">${priceFormatted} / nuit</p>
                <div class="place-description">
                    ${sanitizeHTML(place.description || 'Aucune description disponible.')}
                </div>
                <div class="place-owner">
                    <p><strong>Propriétaire:</strong> ${sanitizeHTML(place.owner.first_name)} ${sanitizeHTML(place.owner.last_name)}</p>
                </div>
                ${place.amenities && place.amenities.length > 0 ? `
                    <div class="place-amenities">
                        <h3>Équipements</h3>
                        <ul>
                            ${place.amenities.map(amenity => `
                                <li>
                                    <span class="amenity-icon">${getAmenityIcon(amenity.name)}</span>
                                    ${sanitizeHTML(amenity.name)}
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        `;

        // Display bookings or calendar based on user role
        if (userId && place.owner.id === userId) {
            loadBookings(placeId);
            const bookingSection = document.getElementById('booking-section');
            if (bookingSection) bookingSection.style.display = 'none';
        } else {
            const bookingSection = document.getElementById('booking-section');
            if (bookingSection) {
                bookingSection.style.display = 'block';
                initBookingForm(placeId, place, confirmedBookings);
            }
        }

        // Always display booked periods for everyone
        displayBookedPeriods(confirmedBookings);

    } catch (error) {
        console.error('Error loading place details:', error);
        showError('Erreur lors du chargement des détails du lieu');
    }
}

// Initialise le formulaire de réservation
function displayBookedPeriods(bookings) {
    const periodsContainer = document.getElementById('booked-periods');
    if (!periodsContainer || !bookings || bookings.length === 0) return;

    periodsContainer.innerHTML = `
        <h3>Périodes réservées</h3>
        <ul class="booked-periods-list">
            ${bookings.map(booking => `
                <li class="booked-period">
                    <span class="icon">📅</span>
                    Du ${new Date(booking.start_date).toLocaleDateString('fr-FR')}
                    au ${new Date(booking.end_date).toLocaleDateString('fr-FR')}
                </li>
            `).join('')}
        </ul>
    `;
}

function initBookingForm(placeId, place, confirmedBookings = []) {
    const form = document.getElementById('booking-form');
    if (!form) return;

    // Convert dates to local time for comparison
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const disabledRanges = [];
    const bookedRanges = [];

    confirmedBookings.forEach(booking => {
        const from = new Date(booking.start_date);
        const to = new Date(booking.end_date);
        from.setHours(0, 0, 0, 0);
        to.setHours(0, 0, 0, 0);

        if (to >= today) {
            disabledRanges.push({ from, to });
            bookedRanges.push({ start: from, end: to });
        }
    });

    // Custom calendar styling with status indicators
    const customCalendarConfig = {
        mode: "range",
        dateFormat: "Y-m-d",
        enableTime: false,
        minDate: today,
        altInput: true,
        altFormat: "d F Y",
        locale: {
            firstDayOfWeek: 1,
            weekdays: {
                shorthand: ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'],
                longhand: ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
            },
            months: {
                shorthand: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sept', 'Oct', 'Nov', 'Déc'],
                longhand: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
            }
        },
        disable: disabledRanges,
        noCalendar: false,
        disableMobile: false,
        onDayCreate: function(dObj, dStr, fp, dayElem) {
            const date = new Date(dObj);
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            // Colorize calendar days based on status
            const currentDate = new Date(dObj);
            currentDate.setHours(0, 0, 0, 0);

            if (currentDate < today) {
                dayElem.classList.add('past-date');
                dayElem.title = 'Date passée';
                return;
            }

            const isBooked = bookedRanges.some(range =>
                currentDate >= range.start && currentDate <= range.end
            );

            if (isBooked) {
                dayElem.classList.add('booked-date');
                dayElem.title = 'Déjà réservé';
                dayElem.innerHTML += '<span class="booked-indicator">•</span>';
            } else {
                dayElem.classList.add('available-date');
                dayElem.title = 'Disponible';
            }
        },
        onChange: function(selectedDates) {
            if (selectedDates.length === 2) {
                const [start, end] = selectedDates;
                start.setHours(0, 0, 0, 0);
                end.setHours(0, 0, 0, 0);

                // Check for overlaps with booked dates
                const hasOverlap = bookedRanges.some(range => {
                    return (start <= range.end && end >= range.start);
                });

                if (hasOverlap) {
                    showError('Ces dates sont déjà réservées');
                    calendar.clear();
                    document.querySelector('.booking-total').innerHTML = '';
                    return;
                }

                // Calculate and display total
                const nights = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
                const total = nights * place.price;
                document.querySelector('.booking-total').innerHTML = `
                    <p>Durée: ${nights} nuit${nights > 1 ? 's' : ''}</p>
                    <p>Total: ${new Intl.NumberFormat('fr-FR', {
                        style: 'currency',
                        currency: 'EUR'
                    }).format(total)}</p>
                `;
            } else {
                document.querySelector('.booking-total').innerHTML = '';
            }
        }
    };

    // Initialize calendar
    const calendar = flatpickr("#booking-dates", customCalendarConfig);

    // Update booking form handler
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const token = getCookie('token');
        if (!token) {
            window.location.href = '/login.html';
            return;
        }

        const button = form.querySelector('button[type="submit"]');
        const spinner = button.querySelector('.loading-spinner');
        button.disabled = true;
        spinner.style.display = 'inline-block';

        try {
            const dates = calendar.selectedDates;
            if (dates.length !== 2) {
                showError('Veuillez sélectionner une période complète');
                return;
            }

            const response = await fetch(`/api/v1/places/${placeId}/bookings`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    start_date: dates[0].toISOString().split('T')[0],
                    end_date: dates[1].toISOString().split('T')[0],
                    message: document.getElementById('message').value
                })
            });

            const result = await response.json();

            if (response.ok) {
                form.reset();
                showSuccess('Votre demande de réservation a été envoyée');
                calendar.clear();

                // Reload the page to refresh bookings
                setTimeout(() => window.location.reload(), 2000);
            } else {
                showError(result.error || 'Erreur lors de la réservation');
            }
        } catch (error) {
            console.error('Error creating booking:', error);
            showError('Erreur lors de la réservation');
        } finally {
            button.disabled = false;
            spinner.style.display = 'none';
        }
    });

    // Show booking calendar immediately
    const calendarElem = document.getElementById('booking-dates');
    if (calendarElem) {
        calendarElem.style.display = 'block';
    }
}

// Charge les réservations pour le propriétaire
async function loadBookings(placeId) {
    try {
        const bookingsList = document.getElementById('bookings-list');
        const placeBookings = document.getElementById('place-bookings');
        if (!bookingsList || !placeBookings) return;

        const token = getCookie('token');
        const response = await fetch(`/api/v1/places/${placeId}/bookings`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) {
            throw new Error('Erreur lors du chargement des réservations');
        }

        const bookings = await response.json();

        if (bookings.length > 0) {
            placeBookings.style.display = 'block';
            bookingsList.innerHTML = bookings.map(booking => `
                <div class="booking-card ${booking.status}">
                    <div class="booking-header">
                        <span class="booking-user">${sanitizeHTML(booking.user.first_name)} ${sanitizeHTML(booking.user.last_name)}</span>
                        <span class="booking-status">
                            ${booking.status === 'pending' ? 'En attente' :
                              booking.status === 'confirmed' ? 'Confirmée' :
                              booking.status === 'cancelled' ? 'Refusée' : booking.status}
                        </span>
                    </div>
                    <div class="booking-dates">
                        Du ${new Date(booking.start_date).toLocaleDateString('fr-FR')}
                        au ${new Date(booking.end_date).toLocaleDateString('fr-FR')}
                    </div>
                    ${booking.message ? `
                        <div class="booking-message">
                            ${sanitizeHTML(booking.message)}
                        </div>
                    ` : ''}
                    ${booking.status === 'pending' ? `
                        <div class="booking-actions">
                            <button onclick="updateBooking('${booking.id}', 'confirm')" class="button success">
                                <span class="icon">✅</span> Valider
                            </button>
                            <button onclick="updateBooking('${booking.id}', 'reject')" class="button danger">
                                <span class="icon">❌</span> Rejeter
                            </button>
                        </div>
                    ` : ''}
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading bookings:', error);
    }
}

// Met à jour le statut d'une réservation
async function updateBooking(bookingId, action) {
    try {
        const token = getCookie('token');
        if (!token) {
            showError('Vous devez être connecté pour effectuer cette action');
            return;
        }

        // Get current placeId from URL
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');

        // Use action-specific endpoints
        const response = await fetch(`/api/v1/places/${placeId}/bookings/${bookingId}/${action}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Échec de la mise à jour de la réservation');
        }

        const message = action === 'confirm' ? 'validée' : 'rejetée';
        showSuccess(`Réservation ${message} avec succès`);

        // Recharge la page pour mettre à jour le calendrier et les réservations
        setTimeout(() => {
            window.location.reload();
        }, 1500);

    } catch (error) {
        console.error('Error updating booking:', error);
        showError(error.message || 'Erreur lors de la mise à jour de la réservation');
    }
}

async function loadReviews(placeId) {
    try {
        const response = await fetch(`/api/v1/places/${placeId}/reviews`);
        const reviews = await response.json();

        const reviewsList = document.getElementById('reviews-list');
        if (reviews.length === 0) {
            reviewsList.innerHTML = '<p>Aucun avis pour le moment.</p>';
            return;
        }

        reviewsList.innerHTML = reviews.map(review => `
            <div class="review-card">
                <div class="review-header">
                    <span class="review-author">${sanitizeHTML(review.user.first_name)} ${sanitizeHTML(review.user.last_name)}</span>
                    <span class="review-rating">
                        ${'⭐'.repeat(review.rating)}
                    </span>
                </div>
                <p class="review-text">${sanitizeHTML(review.text)}</p>
                <div class="review-date">
                    ${new Date(review.created_at).toLocaleDateString('fr-FR')}
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Error loading reviews:', error);
        showError('Failed to load reviews');
    }
}

// Gestion du formulaire d'avis
document.getElementById('add-review-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const token = getCookie('token');
    if (!token) {
        window.location.href = '/login.html';
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    const rating = document.getElementById('rating').value;
    const text = document.getElementById('text').value;

    try {
        const response = await fetch(`/api/v1/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ rating: parseInt(rating), text })
        });

        if (response.ok) {
            document.getElementById('rating').value = '';
            document.getElementById('text').value = '';
            loadReviews(placeId);
        } else {
            const data = await response.json();
            showError(data.error || 'Failed to submit review');
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        showError('Failed to submit review');
    }
});

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.innerHTML = `
        <span class="icon">✅</span>
        ${message}
    `;
    document.querySelector('main').prepend(successDiv);
    setTimeout(() => successDiv.remove(), 5000);
}

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

function sanitizeHTML(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function logout() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = '/login.html';
}
