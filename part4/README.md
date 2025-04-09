# HBnB - Application de Location 🏠

## Description
HBnB est une application web de gestion de locations immobilières, permettant aux utilisateurs de publier et de réserver des logements, ainsi que de laisser des avis.

## Fonctionnalités
- 👥 Gestion des utilisateurs et authentification
- 🏘️ Publication et gestion des logements
- ⭐ Système d'avis et de notation
- 🛠️ Interface d'administration
- 🔍 Recherche et filtrage des logements
- 📅 Système de réservation
  - Validation des réservations par le propriétaire
  - Masquage automatique des logements sur le site pendant leurs périodes de réservation validées
  - Indication claire des périodes "Réservé du [date] au [date]" sur la page du logement
  - Gestion des disponibilités en temps réel

## Installation

1. Créer un environnement virtuel :
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Initialiser la base de données :
```bash
python setup_db.py
```

4. Créer l'administrateur :
```bash
python create_admin.py
```

5. Lancer l'application :
```bash
python run.py
```

## Structure du Projet
```
part4/
├── app/                    # Code backend
│   ├── api/               # Routes API
│   ├── models/           # Modèles de données
│   └── extensions.py     # Extensions Flask
├── static/               # Frontend
│   ├── css/             # Styles par page
│   ├── js/             # Scripts JavaScript
│   ├── images/         # Images
│   └── *.html          # Pages HTML
└── config.py           # Configuration
```

## Compte Administrateur
```
Email: admin@hbnb.io
Mot de passe: admin12345
```

## API Endpoints

### Authentification
- `POST /api/v1/auth/login` : Connexion
- `GET /api/v1/auth/profile` : Profil utilisateur

### Administration
- `GET /api/v1/admin/users` : Liste des utilisateurs
- `POST /api/v1/admin/users` : Création d'utilisateur
- `POST /api/v1/admin/users/<id>/promote` : Promotion admin
- `POST /api/v1/admin/users/<id>/demote` : Rétrogradation admin

### Logements
- `GET /api/v1/places` : Liste des logements
- `POST /api/v1/places` : Création de logement
- `GET /api/v1/places/<id>` : Détails d'un logement
- `PUT /api/v1/places/<id>` : Modification d'un logement
- `DELETE /api/v1/places/<id>` : Suppression d'un logement
### Avis
- `GET /api/v1/places/<id>/reviews` : Avis d'un logement
- `POST /api/v1/places/<id>/reviews` : Création d'avis

### Réservations
- `POST /api/v1/places/<id>/bookings` : Demande de réservation
- `GET /api/v1/places/<id>/bookings` : Liste des réservations d'un logement
- `PUT /api/v1/bookings/<id>/validate` : Validation d'une réservation par le propriétaire
- `PUT /api/v1/bookings/<id>/cancel` : Annulation d'une réservation
- `GET /api/v1/users/bookings` : Liste des réservations de l'utilisateur


## Pages Frontend

- `/` : Page d'accueil avec liste des logements
- `/login.html` : Page de connexion
- `/admin.html` : Interface d'administration
- `/place.html` : Détails d'un logement avec système de réservation
- `/create-place.html` : Création de logement
- `/bookings.html` : Gestion des réservations (propriétaire/locataire)

## Technologies Utilisées

- **Backend** :
  - Flask (Framework web)
  - SQLAlchemy (ORM)
  - JWT (Authentification)
  - SQLite (Base de données)

- **Frontend** :
  - HTML5/CSS3
  - JavaScript (Vanilla)
  - Responsive Design

## Sécurité

- Authentification JWT
- Protection CSRF
- Validation des données
- Hachage des mots de passe
- Protection XSS

## Développement

Pour réinitialiser la base de données :
```bash
python setup_db.py --reset
```

## Notes
- L'application utilise SQLite en développement
- Le mode DEBUG est activé par défaut
- Les fichiers statiques sont servis directement par Flask

## Auteur
[Votre Nom] - 2025
