# 🏠 HBNB - Interface Web & API REST

Une application web complète de gestion de locations, inspirée d'Airbnb, avec une interface utilisateur moderne et une API REST robuste.

## 🖼️ Captures d'écran

### Page d'accueil
![Interface moderne et élégante avec thème bleu professionnel](data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🏠</text></svg>)

### Interface d'administration
![Panel d'administration avec gestion des utilisateurs](data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚙️</text></svg>)

## ✨ Fonctionnalités

- 🔐 **Authentification complète**
  - Système de login/logout
  - Protection des routes sensibles
  - Gestion des rôles (admin/utilisateur)

- 👥 **Gestion des utilisateurs**
  - Interface d'administration
  - Création/modification des utilisateurs
  - Gestion des droits

- 🏡 **Gestion des propriétés**
  - Création d'annonces
  - Recherche et filtrage
  - Affichage détaillé
  - Géolocalisation

- ⭐ **Système d'avis**
  - Notes et commentaires
  - Modération des avis
  - Historique des évaluations

## 🛠️ Technologies

- **Frontend**:
  - HTML5 / CSS3 moderne
  - JavaScript vanilla
  - Interface responsive
  - Design élégant et intuitif

- **Backend**:
  - Python 3.8+
  - Flask 2.x
  - SQLAlchemy ORM
  - JWT Authentication

- **Base de données**:
  - SQLite (développement)
  - PostgreSQL (production)

## 🚀 Installation

```bash
# 1. Cloner le repository
git clone [url-du-repo]
cd part4

# 2. Créer et activer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos paramètres

# 5. Initialiser la base de données
python setup_db.py

# 6. Lancer l'application
python run.py
```

## 🔧 Configuration

Variables d'environnement principales:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=votre-clé-secrète
JWT_SECRET_KEY=votre-clé-jwt
DATABASE_URL=sqlite:///app/hbnb.db
```

## 📱 Utilisation

1. **Interface Administrateur**
   - URL: `/admin.html`
   - Création d'utilisateurs
   - Gestion des droits
   - Supervision des annonces

2. **Création d'annonces**
   - URL: `/create-place.html`
   - Formulaire complet
   - Upload de photos
   - Géolocalisation

3. **Navigation des annonces**
   - Recherche avancée
   - Filtres de prix
   - Vue détaillée
   - Système d'avis

## 🧪 Tests

```bash
# Lancer les tests unitaires
python -m unittest discover tests

# Vérifier la couverture
coverage run -m unittest discover
coverage report
```

## 📚 Documentation

- Documentation API: `/api/v1/docs`
- Guide utilisateur: `GUIDE.md`
- Structure du projet: Voir section Architecture

## 🏗️ Architecture

```
part4/
├── app/
│   ├── api/          # Endpoints API REST
│   ├── models/       # Modèles de données
│   └── services/     # Logique métier
├── static/
│   ├── css/         # Styles
│   ├── js/          # Scripts
│   └── images/      # Assets
└── tests/           # Tests unitaires
```

## 👨‍💻 Auteur

- Baptiste RIVIERE - [GitHub](https://github.com/batrivieredev)

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier `LICENSE` pour plus de détails.

## 🤝 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Me contacter directement par email

---
