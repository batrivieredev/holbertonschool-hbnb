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
