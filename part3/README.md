# HBnB API

API REST pour la gestion de locations de propriétés.

## Installation

1. Créer un environnement virtuel:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

2. Installer les dépendances:
```bash
pip install -e .
```

3. Configurer l'environnement:
```bash
cp .env.example .env
# Modifier les variables dans .env
```

4. Lancer l'application:
```bash
flask run
```

## Documentation API

L'API est documentée avec Swagger UI, accessible à `/api/v1/`.

## Tests

Pour lancer les tests:
```bash
python -m unittest discover tests
```

## Structure du Projet
