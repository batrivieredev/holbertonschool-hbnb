# Guide d'Utilisation de HBNB API

Ce guide détaille les étapes pour installer, configurer et utiliser l'API HBNB.

## Table des Matières

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Lancement](#lancement)
4. [Utilisation de l'API](#utilisation-de-lapi)
5. [Dépannage](#dépannage)

## Installation

### Prérequis

Assurez-vous d'avoir installé :
- Python 3.8 ou supérieur
- PostgreSQL 12 ou supérieur
- git

### Étapes d'installation

1. Cloner le projet :
```bash
git clone [url-du-repo]
cd hbnb-api
```

2. Créer et activer l'environnement virtuel :
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Configuration

1. Copier le fichier d'exemple de configuration :
```bash
cp .env.example .env
```

2. Éditer le fichier .env avec vos paramètres :
```ini
# Configuration de la base de données
DATABASE_URL=postgresql://username:password@localhost/dbname

# Configuration de l'application
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=votre-clé-secrète

# Configuration JWT
JWT_SECRET_KEY=votre-clé-jwt
```

3. Initialiser la base de données :
```bash
python setup_db.py
```

## Lancement

1. Démarrer l'application en mode développement :
```bash
python run.py
```

2. Pour la production, utiliser Gunicorn :
```bash
gunicorn -w 4 -k gevent run:app
```

## Utilisation de l'API

### Documentation Swagger

Accédez à la documentation interactive de l'API :
```
http://localhost:5000/api/v1/
```

### Endpoints Principaux

1. Authentification :
```bash
# Login
POST /api/v1/auth/login
{
    "email": "user@example.com",
    "password": "password123"
}
```

2. Gestion des Places :
```bash
# Créer une nouvelle place
POST /api/v1/places
{
    "title": "Appartement Paris",
    "description": "Bel appartement...",
    "price": 100.0,
    "latitude": 48.8566,
    "longitude": 2.3522
}

# Lister les places
GET /api/v1/places

# Détails d'une place
GET /api/v1/places/{id}
```

3. Gestion des Reviews :
```bash
# Ajouter une review
POST /api/v1/places/{place_id}/reviews
{
    "text": "Superbe endroit !",
    "rating": 5
}
```

### Exemples avec curl

```bash
# Login
curl -X POST http://localhost:5000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password123"}'

# Créer une place (avec token)
curl -X POST http://localhost:5000/api/v1/places \
     -H "Authorization: Bearer <votre-token>" \
     -H "Content-Type: application/json" \
     -d '{"title": "Mon appartement", "description": "..."}'
```

## Dépannage

### Problèmes Courants

1. **Erreur de connexion à la base de données**
   - Vérifier que PostgreSQL est en cours d'exécution
   - Vérifier les informations de connexion dans .env
   - Vérifier les permissions de l'utilisateur de la base de données

2. **Erreurs d'authentification**
   - Vérifier que le token JWT est valide
   - Vérifier que le token est correctement inclus dans le header Authorization

3. **L'application ne démarre pas**
   - Vérifier que tous les packages sont installés : `pip install -r requirements.txt`
   - Vérifier les logs dans la console
   - Vérifier que le port 5000 n'est pas déjà utilisé

### Logs et Debugging

Pour activer le mode debug :
```bash
export FLASK_DEBUG=1
python run.py
```

### Support

Pour plus d'assistance :
1. Consulter les tests dans le dossier `tests/`
2. Vérifier les issues GitHub
3. Contacter l'équipe de développement

---

Pour plus de détails sur l'architecture et le modèle de données, consultez le README.md principal.
