"""
Configuration du package pour l'installation.
Définit les dépendances et métadonnées du projet.
"""

from setuptools import setup, find_packages

setup(
    name='hbnb-api',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'flask>=2.0.0',
        'flask-restx>=0.5.1',
        'flask-sqlalchemy>=2.5.1',
        'flask-jwt-extended>=4.3.1',
        'flask-bcrypt>=0.7.1',
        'python-dotenv>=0.19.0',
    ],
    author='Your Name',
    description='HBnB REST API implementation',
    python_requires='>=3.8',
)
