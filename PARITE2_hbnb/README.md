# HBnB - Part 2: Implementation of Business Logic and API Endpoints

## Introduction
This phase of the **HBnB Project** focuses on implementing the **core functionality** of the application using **Python** and **Flask**. The goal is to build the **Presentation Layer** (API) and the **Business Logic Layer**, ensuring that the application structure follows the documented design from the previous phase.

This part of the project includes setting up the **project structure**, developing the business logic, and implementing **CRUD operations** for managing **users, places, reviews, and amenities**.

## Project Vision and Scope
This part establishes a **functional and scalable foundation** for the application by implementing:

### **1. Business Logic Layer**
- Defining **core models** and logic for managing the application's functionality.
- Establishing **relationships** between entities (e.g., Users, Places, Reviews, Amenities).
- Implementing **data validation** and business rules.
- Using the **Facade pattern** to simplify interactions between the Presentation and Business Logic layers.

### **2. Presentation Layer (API)**
- Defining the **RESTful API endpoints** using **Flask** and **flask-restx**.
- Structuring the API with **clear paths and parameters**.
- Implementing **data serialization** to return **related objects** (e.g., when retrieving a Place, include details such as the owner's name and associated amenities).

## Features Implemented
### **1. Project Structure Setup**
- Organized the project into a **modular architecture**.
- Created packages for **Presentation (API) and Business Logic layers**.

### **2. Business Logic Implementation**
- Developed **core classes**:
  - **User**: Handles user creation and updates.
  - **Place**: Manages property listings.
  - **Review**: Stores user reviews for places.
  - **Amenity**: Lists features available for a place.
- Established **relationships** between these entities.
- Applied **input validation** and **data integrity checks**.

### **3. API Endpoints**
Implemented CRUD operations using Flask-RESTx:
- **Users API**: `POST`, `GET`, `PUT` endpoints to manage users.
- **Places API**: `POST`, `GET`, `PUT` endpoints to handle places.
- **Reviews API**:
  - `POST /reviews/` - Create a new review.
  - `GET /reviews/` - Retrieve all reviews.
  - `GET /reviews/<review_id>` - Get a specific review.
  - `PUT /reviews/<review_id>` - Update a review.
  - `DELETE /reviews/<review_id>` - Delete a review.
  - `GET /places/<place_id>/reviews` - Retrieve reviews for a place.
- **Amenities API**: `POST`, `GET`, `PUT` endpoints to manage amenities.

### **4. Testing and Validation**
- Implemented **unit tests** using `unittest` to verify:
  - Business logic behavior.
  - API response consistency.
  - Handling of **edge cases**.
- Used **Postman** and **cURL** for manual testing.

## Setup and Running the Project
### **1. Install Dependencies**
Make sure you have Python installed, then install required dependencies:
```bash
pip install flask flask-restx
```

### **2. Run the API**
Navigate to the project directory and start the Flask server:
```bash
python run.py
```

The API will be available at:
```
http://127.0.0.1:5000/api/v1/
```

### **3. Running Tests**
Execute the test suite with:
```bash
python -m unittest discover tests/
```

## Learning Objectives
- **Modular Design**: Organizing the project structure using best practices.
- **RESTful API Development**: Implementing endpoints with Flask and flask-restx.
- **Business Logic Implementation**: Applying object-oriented principles to build scalable features.
- **Testing and Debugging**: Validating API functionality using automated tests and debugging techniques.

## Recommended Resources
- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [flask-restx Documentation](https://flask-restx.readthedocs.io/en/latest/)
- [Best Practices for REST API Design](https://restfulapi.net/)
- [Structuring Your Python Project](https://docs.python-guide.org/writing/structure/)
- [Facade Pattern in Python](https://refactoring.guru/design-patterns/facade/python/example)

---
