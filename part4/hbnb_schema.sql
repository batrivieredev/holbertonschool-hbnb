-- Suppression des tables existantes
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS users;

-- Création de la table User
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Création de la table Place
CREATE TABLE IF NOT EXISTS places (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    owner_id TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- Création de la table Review
CREATE TABLE IF NOT EXISTS reviews (
    id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    rating INTEGER,
    user_id TEXT NOT NULL,
    place_id TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    UNIQUE (user_id, place_id)
);

-- Création de la table Amenity
CREATE TABLE IF NOT EXISTS amenities (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Création de la table Place_Amenity (Relation Many-to-Many)
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id TEXT NOT NULL,
    amenity_id TEXT NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);


-- Insertion des équipements initiaux dans la table Amenity
INSERT INTO amenities (id, name) VALUES
    ('1', 'WiFi'),
    ('2', 'Swimming Pool'),
    ('3', 'Air Conditioning');
