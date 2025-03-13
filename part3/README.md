# HBNB API Project

## Installation

1. Installer python3-venv si ce n'est pas déjà fait :
```bash
sudo apt-get install python3-venv
```

2. Créer l'environnement virtuel :
```bash
python3 -m venv venv
```

3. Activer l'environnement virtuel :
```bash
source venv/bin/activate
```

4. Installer les dépendances :
```bash
pip install -r requirements.txt
```

5. Lancer l'application :
```bash
python3 run.py
```

## Tests

Pour exécuter les tests unitaires :
```bash
python3 -m unittest tests/test_amenity_api.py
```

Note: Assurez-vous que l'environnement virtuel est activé avant d'exécuter les commandes.
Pour désactiver l'environnement virtuel :
```bash
deactivate
```

## Diagramme ER de la base de données

```mermaid
erDiagram
    USER {
        int id
        string first_name
        string last_name
        string email
        string password
        datetime created_at
        datetime updated_at
    }

    PLACE {
        int id
        string title
        string description
        float price
        float latitude
        float longitude
        int owner_id
        datetime created_at
        datetime updated_at
    }

    REVIEW {
        int id
        string text
        int rating
        int place_id
        int user_id
        datetime created_at
        datetime updated_at
    }

    AMENITY {
        int id
        string name
        datetime created_at
        datetime updated_at
    }

    PLACE_AMENITY {
        int place_id
        int amenity_id
    }

    %% Relations (les clés étrangères sont gérées ici)
    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : receives
    PLACE ||--o{ PLACE_AMENITY : has
    AMENITY ||--o{ PLACE_AMENITY : is_available_in
