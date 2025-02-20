## Tasks

### 1.

#### Objective

Set up the initial project structure for the HBnB application, ensuring the codebase is organized according to best practices for a modular Python application. The focus is on creating the necessary folders, packages, and files for the Presentation, Business Logic, and Persistence layers while preparing the code to integrate the Facade pattern. Although the Persistence layer will be fully implemented in Part 3 using SQL Alchemy, this task includes setting up the structure and providing the complete implementation of an in-memory repository to handle object storage and validation.

#### Context

Before diving into the implementation of the business logic and API endpoints, it’s essential to have a well-organized project structure. A clear and modular organization will help maintain the codebase, make it easier to integrate new features, and ensure that your application is scalable. Additionally, to simplify the implementation, you are provided with the complete in-memory repository code. This repository will later be replaced by a database-backed solution in Part 3.

In this task, you will:

1.  Set up the structure for the Presentation, Business Logic, and Persistence layers.
2.  Prepare the project to use the Facade pattern for communication between layers.
3.  Implement the in-memory repository to handle object storage and validation.
4.  Plan for future integration of the Persistence layer, even though it won’t be fully implemented in this part.

#### Instructions

\-> [Find the detailed instructions for this task here](/rltoken/-s8prpwrPoVoY-wZCq2Raw "Find the detailed instructions for this task here") <-

#### Expected Outcome

By the end of this task, you should have a well-organized project structure that accommodates the Presentation, Business Logic, and Persistence layers. The codebase should be modular and easy to maintain, with a clear separation of concerns. You’ll also have a functional Flask application that is ready to integrate API endpoints, business logic, and persistence in the upcoming tasks.

The in-memory repository and Facade pattern are now set up to streamline communication between layers. While the persistence layer is only using in-memory storage at this stage, it is designed to be easily replaced with a database-backed solution in Part 3.

#### Resources

1.  **Flask Documentation:** [https://flask.palletsprojects.com/en/stable/](/rltoken/t_B0SLbUFQKqO68vUCgh9g "https://flask.palletsprojects.com/en/stable/")
2.  **Flask-RESTx Documentation:** [https://flask-restx.readthedocs.io/en/latest/](/rltoken/T3KzG_F4pi8xOxm_hv4m3A "https://flask-restx.readthedocs.io/en/latest/")
3.  **Python Project Structure Best Practices:** [https://docs.python-guide.org/writing/structure/](/rltoken/yxYx77NPezEH_Rt9FGfuuQ "https://docs.python-guide.org/writing/structure/")
4.  **Facade Design Pattern in Python:** [https://refactoring.guru/design-patterns/facade/python/example](/rltoken/AMfTkS5vRskcnzTPI6grUQ "https://refactoring.guru/design-patterns/facade/python/example")

  

### 2.

#### Objective

Implement the core business logic classes that define the entities of the HBnB application, including the necessary attributes, methods, and relationships. This task focuses on creating the fundamental models (User, Place, Review, and Amenity) while considering the design choices made by students in Part 1.

#### Context

In Part 1, students designed the Business Logic layer, including defining entities and relationships. This task requires you to implement those designs while adhering to best practices for modular, maintainable code. You may have already created base classes with common attributes (e.g., `id`, `created_at`, and `updated_at`) to be inherited by concrete classes such as `User`, `Place`, `Review`, and `Amenity`.

In this task, you will:

1.  Implement the classes based on your Part 1 design.
2.  Ensure relationships between entities are correctly implemented.
3.  Handle attribute validation and updates according to the requirements.

#### Instructions

\-> [Find the detailed instructions for this task here](/rltoken/yS07eCcaxErW51_HjfYaUA "Find the detailed instructions for this task here") <-

#### Resources

1.  **Python OOP Basics:** [https://realpython.com/python3-object-oriented-programming/](/rltoken/gB7cc0nmujk0WB-CuRW6Vw "https://realpython.com/python3-object-oriented-programming/")
2.  **Designing Classes and Relationships:** [https://docs.python.org/3/tutorial/classes.html](/rltoken/UIITxjVKGbuphwCHWc8U2A "https://docs.python.org/3/tutorial/classes.html")
3.  **Why You Should Use UUIDs:** [https://datatracker.ietf.org/doc/html/rfc4122](/rltoken/ZIUK7VUakGtGbt8er7kOeg "https://datatracker.ietf.org/doc/html/rfc4122")

#### Expected Outcome

By the end of this task, you should have fully implemented core business logic classes (User, Place, Review, Amenity) with the appropriate attributes, methods, and relationships. With these components in place, you will be ready to proceed to implementing the API endpoints in the next task. The implemented classes should support the necessary validation, relationships, and data integrity checks required for the application’s core functionality. Additionally, the relationships between entities should be fully operational, allowing seamless interactions like linking reviews to places or associating amenities with places.

With this solid foundation in place, the business logic will be prepared for further integration with the Presentation and Persistence layers in subsequent tasks.

  

### 3.

#### Objective

Implement the API endpoints needed for managing users in the HBnB application. This task involves setting up CRUD operations (Create, Read, Update) for users, ensuring that these endpoints are integrated with the Business Logic layer. The `DELETE` operation will **not** be implemented for users in this part of the project. Additionally, when retrieving user data, the password should **not** be included in the response. The API interface, return format, and status codes must be clearly defined since black-box testing will be performed later.

In this task, the full implementation for user creation (POST) and retrieval (GET) by ID is provided as a guide. You will be responsible for implementing the retrieval of the list of users (GET /api/v1/users/) and updating user information (PUT /api/v1/users/). The approach for the remaining endpoints follows similar principles and should be implemented analogously. The same applies to the other entities (e.g., Place, Review, Amenity).

In this task, you will:

1.  Set up the `POST`, `GET`, and `PUT` endpoints for managing users.
2.  Implement the logic for handling user-related operations in the Business Logic layer.
3.  Integrate the Presentation layer (API) and Business Logic layer, utilizing the repository pattern.

#### Instructions

\-> [Find the detailed instructions for this task here](/rltoken/m2eQ4O4iOGAkEI-ps_r32A "Find the detailed instructions for this task here") <-

#### Resources

1.  **Flask-RESTx Documentation:** [https://flask-restx.readthedocs.io/en/latest/](/rltoken/T3KzG_F4pi8xOxm_hv4m3A "https://flask-restx.readthedocs.io/en/latest/")
2.  **Testing REST APIs with cURL:** [https://everything.curl.dev/](/rltoken/tA6ap3q1tdnDL67caQc-qg "https://everything.curl.dev/")
3.  **Designing RESTful APIs:** [https://restfulapi.net/](/rltoken/qSLFMktKT5s6HUNZuitwnw "https://restfulapi.net/")

#### Expected Outcome

By the end of this task, you should have fully implemented the core user management endpoints, including the ability to create, read, and update users. The `DELETE` operation will not be implemented for users in this part. The provided implementation guide for the user registration endpoint should serve as a model for implementing the remaining user endpoints as well as endpoints for other entities (e.g., Place, Review, Amenity). The functionality should be documented and tested, ensuring that all user-related operations are handled smoothly within the HBnB application.

  

### 4.

#### Objective

Implement the API endpoints required for managing amenities in the HBnB application. This task involves setting up the endpoints to handle CRUD operations (Create, Read, Update) for amenities, while ensuring integration with the Business Logic layer via the Facade pattern. The `DELETE` operation will not be implemented for amenities in this part of the project.

In this task, you will:

1.  Set up the `POST`, `GET`, and `PUT` endpoints for managing amenities.
2.  Implement the necessary logic for handling amenity-related operations in the Business Logic layer.
3.  Integrate the Presentation layer (API) and Business Logic layer through the Facade.

#### Instructions

\-> [Find the detailed instructions for this task here](/rltoken/dgSGjXTNLi2JYeQv1lhFwQ "Find the detailed instructions for this task here") <-

#### Resources

1.  **Flask-RESTx Documentation:** [https://flask-restx.readthedocs.io/en/latest/](/rltoken/T3KzG_F4pi8xOxm_hv4m3A "https://flask-restx.readthedocs.io/en/latest/")
2.  **Testing REST APIs with cURL:** [https://everything.curl.dev/](/rltoken/tA6ap3q1tdnDL67caQc-qg "https://everything.curl.dev/")
3.  **Designing RESTful APIs:** [https://restfulapi.net/](/rltoken/qSLFMktKT5s6HUNZuitwnw "https://restfulapi.net/")

#### Expected Outcome

By the end of this task, you should have fully implemented the core amenity management endpoints, including the ability to create, read, and update amenities. The `DELETE` operation will not be implemented for amenities in this part. The provided placeholders should guide you in implementing the logic based on the example provided for user registration. The functionality should be documented and tested, ensuring that all amenity-related operations are handled smoothly within the HBnB application.

  

### 5.

#### Objective

Implement the API endpoints needed for managing places in the HBnB application. This task involves setting up CRUD operations (Create, Read, Update) for places, ensuring that these endpoints are integrated with the Business Logic layer through the Facade pattern. The `DELETE` operation will **not** be implemented for places in this part of the project.

Given that the `Place` entity has relationships with other entities, such as `User` (owner) and `Amenity`, you’ll need to handle these relationships carefully while maintaining the integrity of the application logic. The `Review` entity will be implemented in the next task, so it should not be included in this task.

In this task, you will:

1.  Set up the `POST`, `GET`, and `PUT` endpoints for managing places.
2.  Implement the logic for handling place-related operations in the Business Logic layer.
3.  Integrate the Presentation layer (API) and Business Logic layer through the Facade.
4.  Implement validation for specific attributes like `price`, `latitude`, and `longitude`.
5.  Ensure that related data such as `owner` details and `amenities` are properly handled and returned with the Place data.

#### Instructions

\-> [Find the detailed instructions for this task here](/rltoken/1sF0lHD3AL9_wRX26O0YlA "Find the detailed instructions for this task here") <-

### Resources

1.  **Flask-RESTx Documentation:** [https://flask-restx.readthedocs.io/en/latest/](/rltoken/T3KzG_F4pi8xOxm_hv4m3A "https://flask-restx.readthedocs.io/en/latest/")
2.  **Testing REST APIs with cURL:** [https://everything.curl.dev/](/rltoken/tA6ap3q1tdnDL67caQc-qg "https://everything.curl.dev/")
3.  **Designing RESTful APIs:** [https://restfulapi.net/](/rltoken/qSLFMktKT5s6HUNZuitwnw "https://restfulapi.net/")

### Expected Outcome

By the end of this task, you should have implemented the core place management endpoints, including the ability to create, read, and update places. The `DELETE` operation will not be implemented for places in this part. You will have handled the relationships between places, owners, and amenities, including validating specific attributes like price, latitude, and longitude. The functionality should be documented and tested, ensuring smooth operation within the HBnB application.

  

### 6.

#### Objective

Implement the API endpoints needed for managing reviews in the HBnB application. This task involves setting up CRUD operations (Create, Read, Update, Delete) for reviews, ensuring that these endpoints are integrated with the Business Logic layer through the Facade pattern. The `DELETE` operation **will** be implemented for reviews, making it the only entity for which deletion is supported in this part of the project.

In this task, you will:

1.  Set up the `POST`, `GET`, `PUT`, and `DELETE` endpoints for managing reviews.
2.  Implement the logic for handling review-related operations in the Business Logic layer.
3.  Integrate the Presentation layer (API) and Business Logic layer through the Facade.
4.  Implement validation for specific attributes like the text of the review and ensure that the review is associated with both a user and a place.
5.  Update the Place model in `api/v1/places.py` to include the collection of reviews for a place.

#### Instructions

\-> [Find the detailed instructions for this task here](/rltoken/sSsMY_14UyHfZ2CCI5Dwww "Find the detailed instructions for this task here") <-

#### Resources

1.  **Flask-RESTx Documentation:** [https://flask-restx.readthedocs.io/en/latest/](/rltoken/T3KzG_F4pi8xOxm_hv4m3A "https://flask-restx.readthedocs.io/en/latest/")
2.  **Testing REST APIs with cURL:** [https://everything.curl.dev/](/rltoken/tA6ap3q1tdnDL67caQc-qg "https://everything.curl.dev/")
3.  **Designing RESTful APIs:** [https://restfulapi.net/](/rltoken/qSLFMktKT5s6HUNZuitwnw "https://restfulapi.net/")

#### Expected Outcome

By the end of this task, you should have implemented the core review management endpoints, including the ability to create, read, update, and delete reviews. Additionally, you will have implemented the ability to retrieve all reviews associated with a specific place. The `DELETE` operation is introduced here to allow students to practice implementing this functionality for the first time. The functionality should be documented and tested, ensuring that all review-related operations are handled smoothly within the HBnB application.

  

### 7.

#### Objective

This task involves creating and running tests for the endpoints you have developed so far. You will implement validation logic, perform thorough testing using `cURL`, and document the results of those tests. The focus is on ensuring that each endpoint works as expected and adheres to the input/output formats, status codes, and validation rules you have defined in previous tasks.

In this task, you will:

1.  Implement basic validation checks for each of the attributes in your endpoints.
2.  Perform black-box testing using `cURL` and the Swagger documentation generated by Flask-RESTx.
3.  Create a detailed testing report, highlighting both successful and failed cases.

#### Instructions

\-> [Find the detailed instructions for this task here](/rltoken/7Ct5bf7Xxf6hsLBysyF53w "Find the detailed instructions for this task here") <-

#### Expected Outcome

By the end of this task, you should have: - Implemented basic validation for all entity models. - Performed thorough testing using cURL and other tools. - Generated Swagger documentation to confirm that your API is correctly described. - Created and executed unit tests using `unittest` or `pytest`. - Documented the testing process, highlighting both successful cases and edge cases that were handled correctly.

* * *

This task combines both manual and automated testing while guiding students to validate and thoroughly test their implementation. Let me know if any additional information is needed! 
