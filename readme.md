# Raw Feeding API – T2A2

Welcome to the Raw Feeding API, a Flask-based web API designed to help dog owners manage and create raw food recipes for their pets. This application allows users to create, manage, and share recipes, track their dogs' nutritional needs, and generate shopping lists based on selected recipes.

With this app, you can:

- **Create and manage dog profiles**: Add your dogs to the system, including their breed, weight, and age.
- **Create and share recipes**: Design raw food recipes for dogs, specifying ingredients and quantities.
- **Generate shopping lists**: Based on selected recipes, create shopping lists for easy meal preparation.
- **Manage ingredients**: View and search for ingredients, including their nutritional information.
- **User authentication**: Secure login and registration system with admin capabilities.

The app is designed to be user-friendly, with a robust backend powered by Flask and SQLAlchemy, and secure authentication using JWT.

You can view the [GitHub repository here](https://github.com/damian-dp/T2A2-API_Webserver).

## Installation


### Prerequisites:

- Python 3
- PostgreSQL
- Bash (pre-installed on Unix-based systems, available on Windows via WSL)
- Git

<br>

### Unix-based Systems (macOS, Linux) Installation instructions: 

1. Open a terminal instance and navigate to the directory you'd like to clone the repository to.

<br>

2. Clone the GitHub repository via SSH:

    ```sh
    git clone git@github.com:damian-dp/T2A2-API_Webserver.git
    ```

    or via HTTPS:
    
    ```sh
    git clone https://github.com/damian-dp/T2A2-API_Webserver.git
    ```

<br>

3. Navigate to the `/src` directory in the cloned repository:

    ```sh
    cd T2A2-Raw_Feeding_API/src
    ```

<br>

4. Create a virtual environment and activate it:

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

<br>

5. Install the required packages:

    ```sh
    pip3 install -r requirements.txt
    ```

<br>

6. Ensure PostgreSQL is running:

   ```sh
   brew services start postgresql
   ```

    If you don't have PostgreSQL installed via Homebrew, you may need to start it differently based on your installation method. Refer to the [PostgreSQL documentation](https://www.postgresql.org/docs/current/server-start.html) for instructions on starting the server for various installations.


<br>

7. Set up your PostgreSQL database:

   a. Start the PostgreSQL command line client:
      ```sh
      psql
      ```
    
    <br>
   
   b. Create a new database:
      ```sql
      CREATE DATABASE raw_feeding_db;
      ```

    <br>

   c. Create a new user and set a password:
      ```sql
      CREATE USER your_username WITH PASSWORD 'your_password';
      ```

    <br>

   d. Grant database privileges to the new user:
      ```sql
      GRANT ALL PRIVILEGES ON DATABASE raw_feeding_db TO your_username;
      ```

    <br>

    e. Connect to the newly created database:
      ```sql
      \c raw_feeding_db;
      ```

    <br>

    f. Grant schema privileges to the new user:
      ```sql
      GRANT ALL PRIVILEGES ON SCHEMA public TO your_username;
      ```

   g. Exit the PostgreSQL client:
      ```sql
      \q
      ```

<br>

8. Create a `.env` file making sure you're in the `/src` directory and add the following:
   
   ```
   DATABASE_URL=postgresql+psycopg2://username:password@localhost/raw_feeding_db
   JWT_SECRET_KEY=your_jwt_secret_key
   ```

    <br>

    To generate a secure JWT_SECRET_KEY, you can use Python's secrets module. Run this command in your terminal: 

    ```sh
    python3 -c 'import secrets; print(secrets.token_urlsafe(24))'
    ```

    and then copy the generated key into the `.env` file.

<br>

9. Optionally, but recommended for development, you can create a `.flaskenv` file in the `/src` directory to set environment variables for Flask:

    ```
    FLASK_APP=run.py
    FLASK_DEBUG=1
    FLASK_RUN_PORT=5000
    FLASK_ENV=development
    ```

<br>

10. Initialize the database:

    ```sh
    flask create
    flask seed
    ```

<br>

11. Run the application:

    ```sh
    flask run
    ```

<br>

The application should now be running on `http://localhost:5000`.

<br>




### Windows (WSL) Installation instructions:

1. Install [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install) if you haven't already.

<br>

2. Open a WSL terminal and navigate to the directory you'd like to clone the repository to.

<br>

3. Clone the GitHub repository via SSH:

    ```sh
    git clone git@github.com:damian-dp/T2A2-API_Webserver.git
    ```

    or via HTTPS:
    
    ```sh
    git clone https://github.com/damian-dp/T2A2-API_Webserver.git
    ```

<br>

4. Navigate to the `/src` directory in the cloned repository:

    ```sh
    cd T2A2-Raw_Feeding_API/src
    ```

<br>

5. Create a virtual environment and activate it:

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

<br>

6. Install the required packages:

    ```sh
    pip3 install -r requirements.txt
    ```

<br>

7. Ensure PostgreSQL is running:

   ```sh
   sudo service postgresql start
   ```

    If you haven't installed PostgreSQL in your WSL environment, you'll need to do so before proceeding. Refer to the [PostgreSQL documentation](https://www.postgresql.org/docs/current/server-start.html) for instructions on installing and starting the server for WSL.

<br>

8. Set up your PostgreSQL database:

   a. Start the PostgreSQL command line client:
      ```sh
      sudo -u postgres psql
      ```
    
    <br>
   
   b. Create a new database:
      ```sql
      CREATE DATABASE raw_feeding_db;
      ```

    <br>

   c. Create a new user and set a password:
      ```sql
      CREATE USER your_username WITH PASSWORD 'your_password';
      ```

    <br>

   d. Grant database privileges to the new user:
      ```sql
      GRANT ALL PRIVILEGES ON DATABASE raw_feeding_db TO your_username;
      ```

    <br>

    e. Connect to the newly created database:
      ```sql
      \c raw_feeding_db;
      ```

    <br>

    f. Grant schema privileges to the new user:
      ```sql
      GRANT ALL PRIVILEGES ON SCHEMA public TO your_username;
      ```

   g. Exit the PostgreSQL client:
      ```sql
      \q
      ```

<br>

9. Create a `.env` file making sure you're in the `/src` directory and add the following:
   
   ```
   DATABASE_URL=postgresql+psycopg2://username:password@localhost/raw_feeding_db
   JWT_SECRET_KEY=your_jwt_secret_key
   ```

    <br>

    To generate a secure JWT_SECRET_KEY, you can use Python's secrets module. Run this command in your terminal: 

    ```sh
    python3 -c 'import secrets; print(secrets.token_urlsafe(24))'
    ```

    and then copy the generated key into the `.env` file.

<br>

10. Optionally, but recommended for development, you can create a `.flaskenv` file in the `/src` directory to set environment variables for Flask:

    ```
    FLASK_APP=run.py
    FLASK_DEBUG=1
    FLASK_RUN_PORT=5000
    FLASK_ENV=development
    ```

<br>

11. Initialize the database:

    ```sh
    flask create
    flask seed
    ```

<br>

12. Run the application:

    ```sh
    flask run
    ```

<br>

The application should now be running on `http://localhost:5000`.

<br>
<br>


## Third-Party Services, Packages, and Dependencies

The Raw Feeding API utilises several third-party services, packages, and dependencies to enhance its functionality and development process. Here's a detailed list of all packages and their key dependencies:

- `Flask` (version 3.0.3)
    - Werkzeug (version 3.0.3)
    - Jinja2 (version 3.1.4)
    - Click (version 8.1.7)
    - itsdangerous (version 2.2.0)
    - blinker (version 1.8.2)

    Flask is the core framework used to build the application, handling routing, request processing, and response generation. Flask handles routing for all endpoints in the app (e.g., /dogs, /recipes, /ingredients) and manages request processing and response generation for API calls.

<br>

- `SQLAlchemy` (version 2.0.31)
    - typing_extensions (version 4.12.2)

    An SQL toolkit and Object-Relational Mapping (ORM) library for Python. It's used to define models like User, Dog, Recipe, and Ingredient, and to interact with the PostgreSQL database. It's also used to manage the relationships between models, like the many-to-many relationship between Dog and Recipe

<br>

- `Flask-SQLAlchemy` (version 3.1.1)

    An extension for Flask that adds support for SQLAlchemy to the application. It's used to initialize the database and manage database sessions throughout the application. It simplifies database operations and session management throughout the application.

<br>

- `psycopg2` (version 2.9.9)

    The PostgreSQL adapter for Python, allowing the application to connect to and interact with the PostgreSQL database specified in the DATABASE_URL environment variable. It's also used to execute SQL queries and manage database connections.

<br>

- `Flask-JWT-Extended` (version 4.6.0)
    - PyJWT (version 2.8.0)

    An extension that adds support for JSON Web Tokens (JWT) to Flask applications. It's used for user authentication and protecting routes with the @jwt_required() decorator. It protects routes like creating a new recipe or viewing dog profiles, ensuring only authenticated users can access them.

<br>

- `Flask-Marshmallow` (version 1.2.1)
    - marshmallow (version 3.21.3)
    - packaging (version 24.1)

    An integration of Flask and marshmallow. It's used for serializing and deserializing complex data types, particularly for API responses in routes like recipe_routes and ingredient_routes into JSON format.

<br>

- `Marshmallow-SQLAlchemy` (version 1.0.0)

    An integration of marshmallow and SQLAlchemy. It's used to create schemas for the SQLAlchemy models, facilitating easy serialization of database objects like User, Dog, and Recipe in the app.

<br>

- `Flask-Bcrypt` (version 1.0.1)
    - bcrypt (version 4.1.3)

    A Flask extension that provides bcrypt hashing utilities. It's used for securely hashing user passwords before storing them in the database and is used for all password hashing in the app.

<br>

- `python-dotenv` (version 1.0.1)

    A Python module that loads environment variables from a .env file into os.environ. It's used in the config.py file to manage environment variables like database URLs and secret keys for configuration.

<br>

- `email-validator` (version 2.2.0)
    - idna (version 3.7)
    - dnspython (version 2.6.1)

    A library for validating all user email addresses. It's used in user registration and profile update processes to ensure email addresses are in the correct format

<br>

- `bleach` (version 6.1.0)
    - webencodings (version 0.5.1)
    - six (version 1.16.0)

    A library for sanitising and cleaning text based on a whitelist. It's used in the application to sanitise user input, preventing XSS attacks.

<br>

- `python-dateutil` (version 2.9.0.post0)
    - six (version 1.16.0)

    Extensions to the standard Python datetime module. It's used for handling date and time operations, particularly in models like Recipe that involve created_at and updated_at fields.

<br>

These packages and their dependencies work together to provide a robust, secure, and efficient backend for the Raw Feeding App, handling everything from database operations and API serialization to user authentication and input validation.

<br>
<br>

## Problem Statement and Solution

### The Problem: Challenges in Raw Feeding for Dogs

Raw feeding, a diet consisting of uncooked meats, bones, fruits, and vegetables for dogs, has gained popularity in recent years. According to a survey by the University of Guelph, approximately 66% of dog owners have considered raw feeding, with 13% actively practising it [1]. However, this dietary approach comes with significant challenges:

1. **Nutritional Imbalance**: A study published in the Journal of the American Veterinary Medical Association found that 95% of homemade pet diets (including raw diets) were deficient in at least one essential nutrient [2]. This highlights the difficulty in creating balanced raw meals without expert knowledge.

2. **Food Safety Concerns**: The FDA reports that raw pet foods are more likely to be contaminated with bacteria like Salmonella and Listeria compared to processed pet foods [3]. This poses risks not only to pets but also to their human families.

3. **Time and Effort**: Preparing raw meals requires significant time and effort. A survey by PetfoodIndustry.com found that 42% of pet owners who stopped raw feeding cited the time-consuming nature of meal preparation as a primary reason [4].

4. **Cost Management**: Raw feeding can be expensive. The American Kennel Club estimates that raw diets can cost up to $5 per day for a 30-pound dog, compared to $1 per day for premium commercial kibble [5].

5. **Lack of Standardisation**: Unlike commercial pet foods, there's no standardised way to ensure raw diets meet all nutritional requirements, leading to potential health issues in pets.

<br>

### How the Raw Feeding API Solves These Problems

The Raw Feeding API addresses these challenges through a comprehensive, data-driven approach:

1. **Nutritional Balance**:
   - The app includes a database of ingredients with detailed nutritional information (see lines 39-48 in the `cli_controller.py` file).
   - It allows users to create recipes and automatically calculates nutritional totals, ensuring balanced meals (as seen in the `Recipe` model, lines 24-35 in `recipe.py`).

2. **Food Safety Guidance**:
   - While the API can't eliminate all food safety risks, it can provide guidelines and best practices for safe raw food handling and storage.
   - Future updates could include features to track ingredient freshness and suggest safe storage times.

3. **Time and Effort Reduction**:
   - The API streamlines meal planning by allowing users to create, store, and reuse recipes (evident in the `create_recipe` function, lines 20-91 in `recipe_routes.py`).
   - It can generate shopping lists based on selected recipes, saving time on meal preparation.

4. **Cost Management**:
   - By allowing users to input ingredient costs, the API can help calculate the cost per meal and per day for each dog.
   - Users can compare different recipes and ingredients to find cost-effective options while maintaining nutritional balance.

5. **Standardisation and Personalisation**:
   - The API provides a standardised framework for creating raw diets, ensuring consistency across meals.
   - It allows for personalisation based on individual dog profiles (weight, age, breed), as seen in the `Dog` model implementation.

6. **Expert Knowledge Access**:
   - The ingredient database and recipe creation tools encapsulate expert knowledge about canine nutrition, making it accessible to all users.
   - Future versions could incorporate AI-driven recommendations based on the latest veterinary research.

7. **Community and Sharing**:
   - The API supports public and private recipes (line 8 in `recipe.py`), allowing users to share successful meal plans and learn from each other.

By addressing these key challenges, the Raw Feeding API empowers dog owners to confidently and safely implement raw diets for their pets. It combines the benefits of raw feeding with the convenience and assurance of nutritional completeness typically associated with commercial pet foods.

<br>

References:

[1] Empert-Gallegos, A., et al. (2020). "Dog Owner Awareness of Raw Meat-Based Diets and Food Safety Risks." PLoS ONE, 15(4).

[2] Stockman, J., et al. (2013). "Evaluation of recipes of home-prepared maintenance diets for dogs." Journal of the American Veterinary Medical Association, 242(11), 1500-1505.

[3] U.S. Food & Drug Administration. (2021). "Get the Facts! Raw Pet Food Diets can be Dangerous to You and Your Pet."

[4] PetfoodIndustry.com. (2019). "Survey: Why pet owners stop feeding raw pet food diets."

[5] American Kennel Club. (2021). "Raw Dog Food: Dietary Concerns, Benefits, and Risks."

<br>
<br>

## Task Management and Project Progress

Throughout the development of the Raw Feeding API, we utilised Trello as our primary task management tool. This approach allowed us to effectively organise, prioritise, and track the progress of various features and tasks.

### Trello Board

You can view our project's Trello board [here](https://trello.com/b/1oT2Pngq).

The board is organised into the following lists:
- Backlog
- To Do
- In Progress
- Testing
- Done

### Key Milestones

1. Project Initialisation
   - Set up Flask application structure
   - Configure database connection
   - Implement basic user authentication

2. Core Functionality Development
   - Create CRUD operations for Dogs, Recipes, and Ingredients
   - Implement recipe-dog associations
   - Develop nutritional calculation features

3. Advanced Features
   - Add shopping list generation
   - Implement search and filtering capabilities
   - Create admin functionalities

5. Documentation and Deployment
   - Write API documentation
   - Prepare deployment scripts
   - Finalize README and user guide


<br>
<br>

## Database System: Benefits and Drawbacks

The Raw Feeding API utilises PostgreSQL as its underlying database system. This choice brings several benefits and drawbacks to the application:

### Benefits:

1. **ACID Compliance**: PostgreSQL is fully ACID (Atomicity, Consistency, Isolation, Durability) compliant, ensuring data integrity and reliability. This is crucial for the Raw Feeding API, where maintaining accurate relationships between users, dogs, recipes, and ingredients is essential.

2. **Complex Queries**: PostgreSQL excels at handling complex queries, which is beneficial for the Raw Feeding API when dealing with relationships between multiple entities (e.g., searching for recipes based on ingredients or calculating nutritional totals).

3. **Scalability**: As the Raw Feeding API grows and accumulates more users, dogs, and recipes, PostgreSQL can handle large amounts of data efficiently, supporting the application's scalability.

4. **JSON Support**: PostgreSQL's native JSON support is advantageous for storing and querying semi-structured data, which could be useful for future expansions of the API, such as storing custom attributes for recipes or ingredients.

5. **Concurrent Users**: PostgreSQL's excellent handling of concurrent users ensures that the Raw Feeding API can serve multiple users simultaneously without compromising data integrity or performance.

6. **Full-Text Search**: PostgreSQL's full-text search capabilities can be leveraged to implement efficient search functionality for recipes and ingredients in the Raw Feeding API.

7. **Data Integrity**: PostgreSQL's foreign key constraints and cascading updates/deletes help maintain referential integrity between related entities in the Raw Feeding API, such as ensuring that when a recipe is deleted, its associated recipe ingredients are also removed.

### Drawbacks:

1. **Resource Intensity**: PostgreSQL can be more resource-intensive compared to simpler database systems, which might impact the Raw Feeding API's performance on lower-end hosting environments.

2. **Complexity**: The advanced features of PostgreSQL come with increased complexity, which may require more specialised knowledge for optimisation and maintenance of the Raw Feeding API's database.

3. **Vertical Scaling Limitations**: While PostgreSQL can scale vertically (by adding more resources to a single server), it has limitations in horizontal scaling compared to some NoSQL databases. This could potentially impact the Raw Feeding API's ability to distribute data across multiple servers if extreme scalability becomes necessary in the future.

4. **Setup and Configuration**: Initial setup and configuration of PostgreSQL can be more complex compared to some other database systems, potentially increasing the development time for the Raw Feeding API.

5. **Memory Usage**: PostgreSQL's default configuration can sometimes lead to high memory usage, which might require careful tuning for optimal performance of the Raw Feeding API, especially if deployed on memory-constrained environments.

Despite these drawbacks, the benefits of PostgreSQL, particularly its robustness, reliability, and ability to handle complex relationships, make it a suitable choice for the Raw Feeding API. The application's reliance on structured data and complex relationships between entities (users, dogs, recipes, ingredients) aligns well with PostgreSQL's strengths.

<br>
<br>

## Object-Relational Mapping (ORM) System

The Raw Feeding API utilises SQLAlchemy as its Object-Relational Mapping (ORM) system, integrated with Flask through the Flask-SQLAlchemy extension. This ORM plays a crucial role in the application's architecture and functionality.

### Features and Purpose:

1. **Abstraction of Database Operations**: SQLAlchemy abstracts the complexities of SQL queries and database operations, allowing the Raw Feeding API to interact with the database using Python objects and methods. This abstraction simplifies database interactions and reduces the risk of SQL injection vulnerabilities.

2. **Database Agnostic**: While the Raw Feeding API currently uses PostgreSQL, SQLAlchemy's database-agnostic nature allows for potential future migrations to other database systems with minimal code changes.

3. **ORM and Core**: SQLAlchemy provides both high-level ORM functionality and lower-level Core functionality, giving the Raw Feeding API flexibility in how it interacts with the database.

4. **Session Management**: SQLAlchemy's session management handles the complexities of database transactions, ensuring data consistency and integrity in the Raw Feeding API.

5. **Relationship Mapping**: The ORM allows for easy definition and management of relationships between entities (e.g., User-Dog, Recipe-Ingredient), which is crucial for the Raw Feeding API's data model.

6. **Query Construction**: SQLAlchemy provides a powerful query construction API, enabling complex queries to be built programmatically in Python, which is utilised in various parts of the Raw Feeding API, such as recipe searches and filtering.

### Functionalities in the Raw Feeding API:

1. **Model Definition**: SQLAlchemy is used to define the data models for the Raw Feeding API, such as User, Dog, Recipe, and Ingredient. These models are defined in separate files and include column definitions, relationships, and model-specific methods. For example, the Recipe model:


```py
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    # Relationship: One-to-Many with RecipeIngredient model
    # This relationship allows easy access to all ingredients in this recipe
    # The 'cascade' parameter ensures that when a recipe is deleted, its ingredients are also deleted
    ingredients = db.relationship('RecipeIngredient', back_populates='recipe', cascade="all, delete-orphan")

    # Relationship: Many-to-Many with Dog model
    # This relationship allows easy access to all dogs associated with this recipe
    # The 'secondary' parameter specifies the association table for the many-to-many relationship
```


2. **Relationship Handling**: The ORM manages complex relationships in the Raw Feeding API, such as the many-to-many relationship between Dog and Recipe through the `dog_recipe` association table.

3. **Query Execution**: SQLAlchemy is used throughout the application to execute database queries. For example, in the recipe routes, it's used to fetch, create, update, and delete recipes.

4. **Data Validation**: While not directly a feature of SQLAlchemy, the ORM integrates well with Flask-Marshmallow for data serialization and validation in the Raw Feeding API.

5. **Lazy Loading**: SQLAlchemy's lazy loading feature is utilised in the Raw Feeding API to efficiently load related objects only when they are accessed, improving performance.

6. **Cascading Operations**: The ORM's cascading functionality is used in the Raw Feeding API to automatically handle related records. For instance, when a recipe is deleted, its associated recipe ingredients are also removed due to the cascade setting:


```py
    # Relationship: One-to-Many with RecipeIngredient model
    # This relationship allows easy access to all ingredients in this recipe
    # The 'cascade' parameter ensures that when a recipe is deleted, its ingredients are also deleted
    ingredients = db.relationship('RecipeIngredient', back_populates='recipe', cascade="all, delete-orphan")
```


7. **Custom Properties**: SQLAlchemy allows the definition of custom properties on models, which is used in the Recipe model to calculate total calories:


```py
    @property
    def total_calories(self):
        """
        Calculate the total calories for the recipe.
        
        This property sums the calories of each ingredient, multiplied by its quantity.
        It iterates through all RecipeIngredient objects associated with this recipe.
        
        Returns:
            float: The total calories of the recipe.
        """
        return sum(ri.ingredient.calories * ri.quantity for ri in self.ingredients)
```


8. **Query Optimisation**: The ORM's capabilities are leveraged to optimise database queries in the Raw Feeding API. For example, eager loading can be used to fetch related recipes in a single query:

```python
dogs = Dog.query.options(joinedload(Dog.recipes)).filter_by(user_id=current_user_id).all()
```

9. **Event Listeners**: SQLAlchemy's event system can be used to automatically update fields or perform actions before or after certain database operations. For example, updating a dog's age before insert or update:

```python
def calculate_age(target, *args, **kwargs):
    today = datetime.now().date()
    target.age = relativedelta(today, target.date_of_birth).years

db.event.listen(Dog, 'before_insert', calculate_age)
db.event.listen(Dog, 'before_update', calculate_age)
```

10. **Hybrid Properties**: SQLAlchemy's hybrid properties allow for properties that can work both on the Python object level and at the SQL expression level. This can be useful for complex queries:

```python
class Recipe(db.Model):
    # ... other fields ...
    
    @hybrid_property
    def is_high_protein(self):
        return self.total_protein > 30

    @is_high_protein.expression
    def is_high_protein(cls):
        return cls.total_protein > 30

# Can be used in queries
high_protein_recipes = Recipe.query.filter(Recipe.is_high_protein).all()
```

By utilising SQLAlchemy as its ORM, the Raw Feeding API benefits from a powerful, flexible way of interacting with its database, enabling efficient data management and complex query operations while maintaining clean and maintainable code.

<br>
<br>

## Entity-Relationship Diagram (ERD) and Database Design

The Raw Feeding API's database design is represented by a Crow's Foot Entity-Relationship Diagram (ERD). This diagram illustrates the relationships between different entities in our system, providing a clear visual representation of how data is structured and interconnected.

![Raw Feeding API Entity Relationship Diagram](./docs/RawFeeding_ERD.png "Raw Feeding API ERD")

### Relationships and Normalisation

1. **Users and Dogs (One-to-Many)**:
   - A user can have multiple dogs, but each dog belongs to only one user.
   - This relationship is in Third Normal Form (3NF), as the dog's attributes depend only on the dog's primary key (id) and the user_id serves as a foreign key.

2. **Dogs and Recipes (Many-to-Many)**:
   - A dog can have multiple recipes, and a recipe can be associated with multiple dogs.
   - This relationship is implemented using a junction table (DogRecipes), which is in 3NF.
   - The junction table contains only the primary keys of Dogs and Recipes, avoiding transitive dependencies.

3. **Users and Recipes (One-to-Many)**:
   - A user can create multiple recipes, but each recipe is created by only one user.
   - This relationship is in 3NF, with the user_id in the Recipes table serving as a foreign key.

4. **Recipes and Ingredients (Many-to-Many)**:
   - A recipe can have multiple ingredients, and an ingredient can be used in multiple recipes.
   - This relationship is implemented using a junction table (RecipeIngredients), which is in 3NF.
   - The junction table includes quantity and unit information, which directly depend on the combination of recipe_id and ingredient_id.

### Normalisation Comparison

Let's compare the current RecipeIngredients junction table to a less normalised version:

Current (3NF):
```
RecipeIngredients (id, recipe_id, ingredient_id, quantity, unit)
```

Less Normalised (1NF):
```
Recipes (id, user_id, recipe_name, recipe_method, is_public, ingredient1_id, ingredient1_quantity, ingredient1_unit, ingredient2_id, ingredient2_quantity, ingredient2_unit, ...)
```

The 3NF version offers several advantages:
1. Eliminates data redundancy by storing ingredient information separately.
2. Allows for an unlimited number of ingredients per recipe.
3. Simplifies updates and maintenance of ingredient information.
4. Reduces the risk of data anomalies during insertions, updates, or deletions.

### How These Relations Aid Database Design

1. **Flexibility**: The many-to-many relationships between Dogs and Recipes, and between Recipes and Ingredients, allow for maximum flexibility in creating and assigning recipes.

2. **Data Integrity**: Foreign key relationships ensure referential integrity, preventing orphaned records and maintaining data consistency.

3. **Efficient Queries**: The normalised structure allows for efficient querying. For example, to find all recipes for a specific dog:

```sql
SELECT r.* FROM Recipes r
JOIN DogRecipes dr ON r.id = dr.recipe_id
WHERE dr.dog_id = ?
```

4. **Scalability**: The design can easily accommodate new features, such as adding nutritional information to ingredients or additional attributes to recipes, without major structural changes.

5. **Reduced Redundancy**: By normalising to 3NF, we've minimised data duplication, which saves storage space and reduces the risk of data inconsistencies.

6. **Easy Maintenance**: The separation of concerns (e.g., keeping ingredient details separate from recipes) makes it easier to update and maintain the database.

This ERD and its normalised relationships provide a solid foundation for the Raw Feeding API, ensuring data integrity, flexibility, and efficiency in database operations. The design supports the core functionalities of the application while allowing for future expansions and enhancements.

<br>
<br>

## Models and Relationships

The Raw Feeding API utilises several interconnected models to represent the core entities of the application. These models and their relationships are crucial for the efficient operation and data management of the system.

<br>

### User Model

The User model represents registered users of the application. It stores essential information such as username, email, and password hash.


```py
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

```

#### Relationships:
- One-to-Many with Dog model
- One-to-Many with Recipe model

These relationships allow for efficient querying of a user's dogs and recipes. For example:

```python
user = User.query.get(user_id)
user_dogs = user.dogs  # Retrieves all dogs belonging to the user
user_recipes = user.recipes  # Retrieves all recipes created by the user
```

<br>

### Dog Model

The Dog model represents individual dogs in the system, storing information such as name, breed, date of birth, and weight.


```py
class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    profile_image = db.Column(db.String(255))
```


#### Relationships:
- Many-to-One with User model
- Many-to-Many with Recipe model (through DogRecipe association)

The Dog model includes a method to calculate the dog's age:


```py
    def calculate_age(self):
        """
        Calculate and set the dog's age based on its date of birth.
        
        This method computes the difference between the current date and the dog's
        date of birth, setting the 'age' attribute to the number of years.
        """
        today = datetime.now().date()
        self.age = relativedelta(today, self.date_of_birth).years
```


This relationship structure allows for queries such as:

```python
dog = Dog.query.get(dog_id)
owner = dog.user  # Retrieves the dog's owner
dog_recipes = dog.recipes  # Retrieves all recipes associated with the dog
```

<br>

### Recipe Model

The Recipe model represents individual raw feeding recipes, including details like name, description, and instructions.


```py
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```


#### Relationships:
- Many-to-One with User model
- Many-to-Many with Dog model (through DogRecipe association)
- One-to-Many with RecipeIngredient model

The Recipe model includes a property to calculate total calories:


```py
    @property
    def total_calories(self):
        """
        Calculate the total calories for the recipe.
        
        This property sums the calories of each ingredient, multiplied by its quantity.
        It iterates through all RecipeIngredient objects associated with this recipe.
        
        Returns:
            float: The total calories of the recipe.
        """
        return sum(ri.ingredient.calories * ri.quantity for ri in self.ingredients)
```


These relationships enable queries like:

```python
recipe = Recipe.query.get(recipe_id)
creator = recipe.user  # Retrieves the recipe creator
associated_dogs = recipe.dogs  # Retrieves all dogs associated with this recipe
recipe_ingredients = recipe.ingredients  # Retrieves all ingredients in this recipe
```

<br>

### Ingredient Model

The Ingredient model represents individual ingredients that can be used in recipes, including nutritional information.


```py
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    category = db.Column(db.String(64))
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    carbohydrates = db.Column(db.Float)
    fiber = db.Column(db.Float)
```


#### Relationships:
- One-to-Many with RecipeIngredient model

This allows for queries such as:

```python
ingredient = Ingredient.query.get(ingredient_id)
recipes_using_ingredient = [ri.recipe for ri in ingredient.recipe_ingredients]
```

<br>

### RecipeIngredient Model

The RecipeIngredient model serves as a junction table between Recipe and Ingredient, allowing for many-to-many relationships with additional attributes like quantity and unit.


```py
class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
```


#### Relationships:
- Many-to-One with Recipe model
- Many-to-One with Ingredient model

This model enables queries like:

```python
recipe_ingredient = RecipeIngredient.query.filter_by(recipe_id=recipe_id, ingredient_id=ingredient_id).first()
recipe = recipe_ingredient.recipe
ingredient = recipe_ingredient.ingredient
quantity = recipe_ingredient.quantity
unit = recipe_ingredient.unit
```

<br>

### DogRecipe Association

The DogRecipe association table facilitates the many-to-many relationship between Dog and Recipe models.


```py
dog_recipe = db.Table('dog_recipe',
    # Foreign key referencing the Dog model's id
    db.Column('dog_id', db.Integer, db.ForeignKey('dog.id'), primary_key=True),
    # Foreign key referencing the Recipe model's id
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)
```


This association allows for queries such as:

```python
dog = Dog.query.get(dog_id)
dog_recipes = dog.recipes

recipe = Recipe.query.get(recipe_id)
dogs_using_recipe = recipe.dogs
```

<br>

### How Relationships Aid Database Implementation

1. **Efficient Data Retrieval**: The relationships allow for easy and efficient retrieval of related data. For example, getting all recipes for a specific dog or all ingredients in a recipe can be done with simple queries.

2. **Data Integrity**: Foreign key relationships ensure referential integrity, preventing orphaned records and maintaining data consistency.

3. **Flexible Queries**: The ORM relationships enable complex queries making it easier to implement features like filtering recipes by ingredients or finding all dogs on a specific diet.

4. **Cascading Operations**: Relationships can be set up with cascading deletes, ensuring that when a parent record is deleted, all related child records are also removed, maintaining database consistency.

5. **Lazy Loading**: SQLAlchemy's lazy loading feature allows for efficient database queries, only fetching related data when it's actually accessed.

These model relationships form the backbone of the Raw Feeding API, enabling complex operations like recipe creation, nutritional analysis, and personalized feeding plans for dogs. The structure allows for scalability and easy addition of new features as the application grows.


<br>
<br>

## API Endpoints

This section provides detailed information about the available API endpoints, their usage, and expected responses.

<br>

### Auth Routes:

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Register new user | `/auth/register` | POST | null | null |

<br>

**Example Request Body**:
  ```json
  {
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepassword123"
  }
  ```

<br>

**Example Success Response** (201 Created):
  ```json
  {
    "message": "User registered successfully",
    "user": {
      "id": 1,
      "username": "newuser",
      "email": "newuser@example.com"
    }
  }
  ```

<br>

**Error Responses**:
  
  - 400 Bad Request:

    ```json
    {
      "error": "Invalid input",
      "message": "Username must be 3-20 characters long and contain only letters, numbers, and underscores."
    }
    ```
    ```json
    {
      "error": "Invalid input",
      "message": "Invalid email format."
    }
    ```
    ```json
    {
      "error": "Invalid input",
      "message": "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character."
    }
    ```

    <br>

  - 409 Conflict:
    
    ```json
    {
      "error": "Conflict",
      "message": "Username already exists."
    }
    ```
    ```json
    {
      "error": "Conflict",
      "message": "Email already registered."
    }
    ```

<br>
<br>

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| User login | `/auth/login` | POST | JWT in header | null |

<br>

**Example Request Body**:
  ```json
  {
    "username": "existinguser",
    "password": "correctpassword123"
  }
  ```

<br>

**Example Success Response** (201 Created):
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "existinguser",
      "email": "existinguser@example.com"
    }
  }
  ```

<br>

**Error Responses**:
  
  - 400 Bad Request:

    ```json
    {
      "error": "Invalid input",
      "message": "Username and password are required."
    }
    ```

    <br>

  - 401 Unauthorised:
    
    ```json
    {
      "error": "Unauthorised",
      "message": "Invalid username or password."
    }
    ```

<br>
<br>

### User Routes:

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Get users | `/users` | GET | JWT in header | `include_dogs`, `include_recipes` |

<br>

    NOTE: If the user is an admin all users will be returned, otherwise if the user is not an admin only the user that is logged in will be returned.

<br>

**Example Success Response**:

- 200 OK (Non-admin user, no query parameters): `/users`
  
  ```json
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_admin": false,
  }
  ```

<br>

- 200 OK (Non-admin user, with query parameters): `/users?include_dogs=true&include_recipes=true`
  
  ```json
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_admin": false,
    "dog_ids": [1, 2],
    "recipe_ids": [1, 2, 3]
  }
  ```

<br>

- 200 OK (Admin user, no query parameters): `/users`

  ```json
  [
    {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "is_admin": false
    },
    {
      "id": 2,
      "username": "jane_smith",
      "email": "jane@example.com",
      "is_admin": true
    }
  ]
  ```

<br>

- 200 OK (Admin user, with query parameters): `/users?include_dogs=true&include_recipes=true`

  ```json
  [
    {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "is_admin": false,
      "dog_ids": [1, 2],
      "recipe_ids": [1, 2, 3]
    },
    {
      "id": 2,
      "username": "jane_smith",
      "email": "jane@example.com",
      "is_admin": true,
      "dog_ids": [3],
      "recipe_ids": [4, 5]
    }
  ]
  ```

<br>

**Error Responses**:
  
- 403 Forbidden:

  ```json
  {
    "error": "Access denied",
    "message": "You do not have permission to view all users. This endpoint is restricted to admin users only."
  }
  ```

<br>

- 500 Internal Server Error:

  ```json
  {
    "error": "An unexpected error occurred",
    "details": "Error details here"
  }
  ```

<br>
<br>

---


<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Get specific user | `/users/<user_id>` | GET | JWT in header | `include_dogs`, `include_recipes` |

<br>

    NOTE: If the user is an admin they can view any user, otherwise if the user is not an admin they can only view their own profile.

<br>

**Example Success Response**:

- 200 OK: `/users/1`
  
  ```json
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_admin": false
  }
  ```

<br>

- 200 OK: `/users/1?include_dogs=true&include_recipes=true`

  ```json
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_admin": false,
    "dog_ids": [1, 2],
    "recipe_ids": [1, 2, 3]
  }
  ```

<br>

**Error Responses**:
  
- 400 Bad Request:

  ```json
  {
    "error": "Invalid user_id. Must be a positive integer."
  }
  ```

- 403 Forbidden:

  ```json
  {
    "error": "Unauthorised. You can only view your own profile."
  }
  ```

- 404 Not Found:

  ```json
  {
    "error": "User not found"
  }
  ```

<br>
<br>

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Update user | `/users/<user_id>` | PUT, PATCH | JWT in header | None |

<br>

    NOTE: If the user is an admin they can update any user, otherwise if the user is not an admin they can only update their own profile. Only users who are admins can use the is_admin field in the request body.

<br>

**Example Request Body**:
  ```json
  {
    "username": "new_username",
    "email": "newemail@example.com",
    "password": "newPassword123!"
  }
  ```

<br>

**Example Success Response**:

- 200 OK: `/users/1`
  
  ```json
  {
    "id": 1,
    "username": "new_username",
    "email": "newemail@example.com",
    "is_admin": false
  }
  ```

<br>

**Error Responses**:
  
- 400 Bad Request:

  ```json
  {
    "error": "Invalid username. Username must be 3-20 characters long and contain only letters, numbers, and underscores."
  }
  ```

  ```json
  {
    "error": "Invalid email address. Please provide a valid email format."
  }
  ```

  ```json
  {
    "error": "Invalid password. Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
  }
  ```

- 403 Forbidden:

  ```json
  {
    "error": "Unauthorised. You can only update your own profile."
  }
  ```

  ```json
  {
    "error": "Unauthorised. Only admins can update the admin status."
  }
  ```

- 404 Not Found:

  ```json
  {
    "error": "User not found"
  }
  ```

<br>
<br>

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Delete user | `/users/<user_id>` | DELETE | JWT in header | None |

<br>

    NOTE: If the user is an admin they can delete any user, otherwise if the user is not an admin they can only delete their own account.

<br>

**Example Success Response**:

- 200 OK: `/users/1`
  
  ```json
  {
    "message": "User deleted successfully"
  }
  ```

<br>

**Error Responses**:
  
- 400 Bad Request:

  ```json
  {
    "error": "Invalid user_id. Must be a positive integer."
  }
  ```

- 403 Forbidden:

  ```json
  {
    "error": "Unauthorized. You can only delete your own account."
  }
  ```

- 404 Not Found:

  ```json
  {
    "error": "User not found"
  }
  ```

<br>
<br>

### Dog Routes:

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Create dog | `/dogs` | POST | JWT in header | None |

<br>

**Example Request Body**:
  ```json
  {
    "name": "Buddy",
    "breed": "Labrador",
    "date_of_birth": "2020-01-15",
    "weight": 25.5,
    "profile_image": "https://example.com/dog_image.jpg"
  }
  ```

<br>

**Example Success Response**:

- 201 Created: `/dogs`
  
  ```json
  {
    "id": 1,
    "name": "Buddy",
    "breed": "Labrador",
    "date_of_birth": "2020-01-15",
    "weight": 25.5,
    "profile_image": "https://example.com/dog_image.jpg",
    "user_id": 1
  }
  ```

<br>

**Error Responses**:
  
- 400 Bad Request:

  ```json
  {
    "error": "Invalid dog name. Name must be 1-50 characters long."
  }
  ```

  ```json
  {
    "error": "Invalid dog breed. Breed must be 1-50 characters long."
  }
  ```

  ```json
  {
    "error": "Invalid date of birth. Please provide a valid date in the format YYYY-MM-DD."
  }
  ```

  ```json
  {
    "error": "Invalid weight. Weight must be a positive number less than 200kg."
  }
  ```

  ```json
  {
    "error": "Invalid profile image URL. Must be a string with max length 255."
  }
  ```

<br>
<br>

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Get all dogs | `/dogs` | GET | JWT in header | None |

<br>

    NOTE: If the user is an admin they can view all dogs, otherwise if the user is not an admin they can only view their own dogs.

<br>

**Example Success Response**:

- 200 OK (User is admin):
  
  ```json
  [
    {
      "id": 1,
      "name": "Buddy",
      "breed": "Labrador",
      "date_of_birth": "2020-01-15",
      "weight": 25.5,
      "profile_image": "https://example.com/dog_image.jpg",
      "user_id": 1,
      "recipes": [1, 2]
    },
    {
      "id": 2,
      "name": "Max",
      "breed": "German Shepherd",
      "date_of_birth": "2019-05-20",
      "weight": 30.2,
      "profile_image": "https://example.com/max_image.jpg",
      "user_id": 1,
      "recipes": [1]
    }
  ]
  ```

<br>

- 200 OK (User is not admin):
  
  ```json
    {
        "id": 1,
        "name": "Buddy",
        "breed": "Labrador",
        "date_of_birth": "2020-01-15",
        "weight": 25.5,
        "profile_image": "https://example.com/dog_image.jpg",
        "user_id": 1,
        "recipes": [1, 2]
    }
  ```

<br>

**Error Responses**:
  
- 500 Internal Server Error:

  ```json
  {
    "error": "An unexpected error occurred",
    "details": "Error details here"
  }
  ```

<br>
<br>

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Get specific dog | `/dogs/<dog_id>` | GET | JWT in header | None |

<br>

    NOTE: If the user is an admin they can view all dogs, otherwise if the user is not an admin they can only view their own dogs.

<br>

**Example Success Response**:

- 200 OK:
  
  ```json
  {
    "id": 1,
    "name": "Buddy",
    "breed": "Labrador",
    "date_of_birth": "2020-01-15",
    "weight": 25.5,
    "profile_image": "https://example.com/dog_image.jpg",
    "user_id": 1,
    "recipes": [1, 2]
  }
  ```

<br>

**Error Responses**:
  
- 403 Forbidden:

  ```json
  {
    "error": "Access denied",
    "message": "You do not have permission to view this dog. You can only view dogs that you own."
  }
  ```

<br>

- 404 Not Found:

  ```json
  {
    "error": "Dog not found"
  }
  ```

<br>
<br>

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Update dog | `/dogs/<dog_id>` | PUT, PATCH | JWT in header | None |

<br>

    NOTE: If the user is an admin they can update any dog, otherwise if the user is not an admin they can only update their own dogs.

<br>

**Example Request Body**:
  ```json
  {
    "name": "Buddy",
    "breed": "Labrador Retriever",
    "date_of_birth": "2020-01-15",
    "weight": 27.5,
    "profile_image": "https://example.com/updated_dog_image.jpg"
  }
  ```

<br>

**Example Success Response**:

- 200 OK: `/dogs/1`
  
  ```json
  {
    "id": 1,
    "name": "Buddy",
    "breed": "Labrador Retriever",
    "date_of_birth": "2020-01-15",
    "weight": 27.5,
    "profile_image": "https://example.com/updated_dog_image.jpg",
    "user_id": 1
  }
  ```

<br>

**Error Responses**:
  
- 400 Bad Request:

  ```json
  {
    "error": "Invalid dog name. Name must be 1-50 characters long."
  }
  ```

  ```json
  {
    "error": "Invalid dog breed. Breed must be 1-50 characters long."
  }
  ```

  ```json
  {
    "error": "Invalid date format. Use YYYY-MM-DD."
  }
  ```

  ```json
  {
    "error": "Invalid weight. Weight must be a positive number less than 200 (assuming kg)."
  }
  ```

  ```json
  {
    "error": "Invalid profile image URL."
  }
  ```

<br>

- 403 Forbidden:

  ```json
  {
    "error": "Access denied",
    "message": "You do not have permission to update this dog. You can only update dogs that you own."
  }
  ```

<br>

- 404 Not Found:

  ```json
  {
    "error": "Dog not found"
  }
  ```

<br>
<br>

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Delete dog | `/dogs/<dog_id>` | DELETE | JWT in header | None |

<br>

    NOTE: If the user is an admin they can delete any dog, otherwise if the user is not an admin they can only delete their own dogs.

<br>

**Example Success Response**:

- 200 OK:
  
  ```json
  {
    "msg": "Dog deleted"
  }
  ```

<br>

**Error Responses**:
  
- 400 Bad Request:

  ```json
  {
    "error": "Invalid dog_id. Must be a positive integer."
  }
  ```

<br>

- 403 Forbidden:

  ```json
  {
    "error": "Access denied",
    "message": "You do not have permission to delete this dog. You can only delete dogs that you own."
  }
  ```

<br>

- 404 Not Found:

  ```json
  {
    "error": "Dog not found"
  }
  ```

<br>
<br>

### Ingredient Routes:

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Get all ingredients | `/ingredients` | GET | None | None |

<br>

**Example Success Response**:

- 200 OK:
  
    ```json
    [
        {
            "calories": 165.0,
            "carbohydrates": 0.0,
            "category": "Meat",
            "fat": 3.6,
            "fiber": null,
            "id": 1,
            "minerals": null,
            "name": "Chicken Breast",
            "protein": 31.0,
            "vitamins": null
        },
        {
            "calories": 216.0,
            "carbohydrates": 45.0,
            "category": "Grain",
            "fat": 1.8,
            "fiber": null,
            "id": 2,
            "minerals": null,
            "name": "Brown Rice",
            "protein": 5.0,
            "vitamins": null
        },
        {
            "calories": 55.0,
            "carbohydrates": 11.2,
            "category": "Vegetable",
            "fat": 0.6,
            "fiber": null,
            "id": 3,
            "minerals": null,
            "name": "Broccoli",
            "protein": 3.7,
            "vitamins": null
        },
        {
            "calories": 208.0,
            "carbohydrates": 0.0,
            "category": "Fish",
            "fat": 13.0,
            "fiber": null,
            "id": 4,
            "minerals": null,
            "name": "Salmon",
            "protein": 20.0,
            "vitamins": null
        },
        {
            "calories": 86.0,
            "carbohydrates": 20.0,
            "category": "Vegetable",
            "fat": 0.1,
            "fiber": null,
            "id": 5,
            "minerals": null,
            "name": "Sweet Potato",
            "protein": 1.6,
            "vitamins": null
        }
    ]
    ```

<br>

**Error Responses**:
  
- 500 Internal Server Error:

  ```json
  {
    "error": "An unexpected error occurred"
  }
  ```

<br>
<br>

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Get specific ingredient | `/ingredients/<ingredient_id>` | GET | None | None |

<br>

**Example Success Response**:

- 200 OK:
  
  ```json
    {
        "calories": 165.0,
        "carbohydrates": 0.0,
        "category": "Meat",
        "fat": 3.6,
        "fiber": null,
        "id": 1,
        "minerals": null,
        "name": "Chicken Breast",
        "protein": 31.0,
        "vitamins": null
    }
  ```

<br>

**Error Responses**:
  
- 404 Not Found:

  ```json
  {
    "error": "Ingredient not found"
  }
  ```

<br>

- 500 Internal Server Error:

  ```json
  {
    "error": "An unexpected error occurred"
  }
  ```

<br>
<br>

### Recipe Routes:

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Create recipe | `/recipes` | POST | JWT in header | None |

<br>

    NOTE: Users who are admins can assign any dog to a recipe, otherwise users who are not admins can only assign their own dogs to a recipe.

<br>

**Request Body**:
```json
{
  "name": "Chicken and Rice",
  "description": "A simple and nutritious meal for dogs",
  "instructions": "1. Cook chicken. 2. Cook rice. 3. Mix together.",
  "is_public": true,
  "ingredients": [
    {
      "ingredient_id": 1,
      "quantity": 200,
      "unit": "grams"
    },
    {
      "ingredient_id": 2,
      "quantity": 100,
      "unit": "grams"
    }
  ],
  "dog_ids": [1, 2]
}
```

<br>

**Example Success Response**:

- 201 Created:
  
  ```json
  {
    "id": 1,
    "name": "Chicken and Rice",
    "description": "A simple and nutritious meal for dogs",
    "instructions": "1. Cook chicken. 2. Cook rice. 3. Mix together.",
    "is_public": true,
    "ingredients": [
      {
        "ingredient_id": 1,
        "name": "Chicken",
        "quantity": 200,
        "unit": "grams"
      },
      {
        "ingredient_id": 2,
        "name": "Rice",
        "quantity": 100,
        "unit": "grams"
      }
    ],
    "dogs": [1, 2],
    "user_id": 1
  }
  ```

<br>

**Error Responses**:
  
- 400 Bad Request:

  ```json
  {
    "error": "At least one dog must be associated with the recipe."
  }
  ```

  ```json
  {
    "error": "Invalid recipe name. Recipe name should be 3-100 characters long."
  }
  ```

  ```json
  {
    "error": "Invalid recipe instructions. Must be a non-empty string."
  }
  ```

  ```json
  {
    "error": "Invalid recipe description. Must be a string."
  }
  ```

  ```json
  {
    "error": "Invalid dog_ids. Must be a non-empty list of integers."
  }
  ```

  ```json
  {
    "error": "is_public must be a boolean value."
  }
  ```

  ```json
  {
    "error": "Invalid ingredient_id: {ingredient_id}. Must be a positive integer."
  }
  ```

  ```json
  {
    "error": "Invalid unit for ingredient {ingredient_id}. Must be a non-empty string with max length 20."
  }
  ```

  ```json
  {
    "error": "Invalid quantity for ingredient {ingredient_id}. Quantity must be a positive number."
  }
  ```

  ```json
  {
    "error": "Ingredient with id {ingredient_id} not found. Please use a valid ingredient ID."
  }
  ```

  ```json
  {
    "error": "Invalid ingredient name for id {ingredient_id}. Ingredient name should be 2-50 characters long and contain only letters, numbers, spaces, and hyphens."
  }
  ```

<br>

- 403 Forbidden:

  ```json
  {
    "error": "You don't have permission to assign dog with id {dog_id} to this recipe"
  }
  ```

<br>

- 404 Not Found:

  ```json
  {
    "error": "Dog with id {dog_id} not found"
  }
  ```

<br>
<br>

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Get all recipes | `/recipes` | GET | JWT in header | None |

<br>

    NOTE: If the user is not an admin, they will only see their own recipes and recipes that have is_public set to true. If the user is an admin, they will see all recipes.

<br>

**Example Success Response**:

- 200 OK:
  
  ```json
    [
        {
            "name": "Chicken and Rice Bowl",
            "description": "A balanced meal for active dogs",
            "id": 1,
            "is_public": true,
            "user_id": 4,
            "dog_ids": [
                1,
                2
            ],
            "ingredients": [
                {
                    "id": 1,
                    "ingredient_id": 1,
                    "ingredient_name": "Chicken Breast",
                    "quantity": 100.0,
                    "recipe_id": 1,
                    "unit": "grams"
                },
                {
                    "id": 2,
                    "ingredient_id": 2,
                    "ingredient_name": "Brown Rice",
                    "quantity": 50.0,
                    "recipe_id": 1,
                    "unit": "grams"
                },
                {
                    "id": 3,
                    "ingredient_id": 3,
                    "ingredient_name": "Broccoli",
                    "quantity": 30.0,
                    "recipe_id": 1,
                    "unit": "grams"
                }
            ],
            "instructions": "1. Cook chicken breast. 2. Mix all ingredients together.",
            "created_at": "2024-07-24T06:24:10.366410",
            "updated_at": "2024-07-24T06:24:10.366415"
        },
        {
            "name": "Special Chicken Bowl",
            "description": "A balanced meal for active dogs",
            "id": 2,
            "is_public": true,
            "user_id": 5,
            "dog_ids": [
                3
            ],
            "ingredients": [
                {
                    "id": 1,
                    "ingredient_id": 1,
                    "ingredient_name": "Chicken Breast",
                    "quantity": 100.0,
                    "recipe_id": 1,
                    "unit": "grams"
                },
                {
                    "id": 2,
                    "ingredient_id": 2,
                    "ingredient_name": "Brown Rice",
                    "quantity": 50.0,
                    "recipe_id": 1,
                    "unit": "grams"
                },
                {
                    "id": 3,
                    "ingredient_id": 3,
                    "ingredient_name": "Broccoli",
                    "quantity": 30.0,
                    "recipe_id": 1,
                    "unit": "grams"
                }
            ],
            "instructions": "1. Cook chicken breast. 2. Mix all ingredients together.",
            "created_at": "2024-07-24T06:24:10.366410",
            "updated_at": "2024-07-24T06:24:10.366415"
        },
    ]
  ```

<br>

**Error Responses**:
  
- 500 Internal Server Error:

  ```json
  {
    "error": "An unexpected error occurred"
  }
  ```

<br>
<br>

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Get specific recipe | `/recipes/<recipe_id>` | GET | JWT in header | None |

<br>

    NOTE: If the user is not an admin, they will only see their own recipes and recipes that have is_public set to true. If the user is an admin, they will see all recipes.

<br>

**Example Success Response**:

- 200 OK:
  
  ```json
    {
        "name": "Chicken and Rice Bowl",
        "description": "A balanced meal for active dogs",
        "id": 1,
        "is_public": true,
        "user_id": 4,
        "dog_ids": [
            1,
            2
        ],
        "ingredients": [
            {
                "id": 1,
                "ingredient_id": 1,
                "ingredient_name": "Chicken Breast",
                "quantity": 100.0,
                "recipe_id": 1,
                "unit": "grams"
            },
            {
                "id": 2,
                "ingredient_id": 2,
                "ingredient_name": "Brown Rice",
                "quantity": 50.0,
                "recipe_id": 1,
                "unit": "grams"
            },
            {
                "id": 3,
                "ingredient_id": 3,
                "ingredient_name": "Broccoli",
                "quantity": 30.0,
                "recipe_id": 1,
                "unit": "grams"
            }
        ],
        "instructions": "1. Cook chicken breast. 2. Mix all ingredients together.",
        "created_at": "2024-07-24T06:24:10.366410",
        "updated_at": "2024-07-24T06:24:10.366415"
    }
  ```

<br>

**Error Responses**:
  
- 403 Forbidden:

  ```json
  {
    "error": "Access denied",
    "message": "You do not have permission to view this recipe. You can only view your own recipes or public recipes."
  }
  ```

- 404 Not Found:

  ```json
  {
    "error": "Recipe not found"
  }
  ```

<br>
<br>

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Update recipe | `/recipes/<recipe_id>` | PUT, PATCH | JWT in header | None |

<br>

**Example Request Body** (all fields are optional):
```json
{
  "name": "Updated Chicken and Rice",
  "description": "An updated simple and nutritious meal for dogs",
  "instructions": "1. Cook chicken. 2. Cook rice. 3. Mix together. 4. Serve warm.",
  "is_public": true,
  "ingredients": [
    {
      "ingredient_id": 1,
      "quantity": 250,
      "unit": "grams"
    },
    {
      "ingredient_id": 2,
      "quantity": 150,
      "unit": "grams"
    }
  ],
  "dog_ids": [1, 2, 3]
}
```

<br>

**Example Success Response**:

- 200 OK:
  
  ```json
  {
    "id": 1,
    "name": "Updated Chicken and Rice",
    "description": "An updated simple and nutritious meal for dogs",
    "instructions": "1. Cook chicken. 2. Cook rice. 3. Mix together. 4. Serve warm.",
    "is_public": true,
    "ingredients": [
      {
        "id": 1,
        "ingredient_id": 1,
        "name": "Chicken",
        "quantity": 250,
        "unit": "grams"
      },
      {
        "id": 2,
        "ingredient_id": 2,
        "name": "Rice",
        "quantity": 150,
        "unit": "grams"
      }
    ],
    "dogs": [1, 2, 3],
    "user_id": 1
  }
  ```

<br>

**Error Responses**:
  
- 400 Bad Request:

  ```json
  {
    "error": "Invalid recipe name. Recipe name should be 3-100 characters long."
  }
  ```

  ```json
  {
    "error": "Invalid recipe instructions. Must be a non-empty string."
  }
  ```

  ```json
  {
    "error": "Invalid recipe description. Must be a string."
  }
  ```

  ```json
  {
    "error": "Invalid dog_ids. Must be a non-empty list of integers."
  }
  ```

  ```json
  {
    "error": "Invalid quantity for ingredient {ingredient_id}. Quantity must be a positive number."
  }
  ```

  ```json
  {
    "error": "Ingredient with id {ingredient_id} not found. Please use a valid ingredient ID."
  }
  ```

  ```json
  {
    "error": "Invalid ingredient name for id {ingredient_id}. Ingredient name should be 2-50 characters long and contain only letters, numbers, spaces, and hyphens."
  }
  ```

<br>

- 403 Forbidden:

  ```json
  {
    "error": "Access denied",
    "message": "You do not have permission to update this recipe. You can only update your own recipes."
  }
  ```

  ```json
  {
    "error": "You don't have permission to assign dog with id {dog_id} to this recipe"
  }
  ```

<br>

- 404 Not Found:

  ```json
  {
    "error": "Recipe not found"
  }
  ```

  ```json
  {
    "error": "Dog with id {dog_id} not found"
  }
  ```

<br>
<br>

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Delete recipe | `/recipes/<recipe_id>` | DELETE | JWT in header | None |

<br>

    NOTE: If the user is not an admin, they will only be able to delete their own recipes. If the user is an admin, they will be able to delete any recipe.

<br>

**Example Success Response**:

- 200 OK:
  
  ```json
  {
    "message": "Recipe deleted successfully"
  }
  ```

<br>

**Error Responses**:

- 403 Forbidden:

  ```json
  {
    "error": "Access denied",
    "message": "You do not have permission to delete this recipe. You can only delete your own recipes."
  }
  ```

<br>

- 404 Not Found:

  ```json
  {
    "error": "Recipe not found"
  }
  ```

<br>
<br>

### Shopping List Routes:

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Generate Shopping List | `/shopping-list` | GET | JWT in header | `recipe_ids` |

<br>

    NOTE: You can include multiple recipe_ids in the URL query parameter to combine ingredients from multiple recipes. The quantities of each ingredient in each recipe will be added together to create the final shopping list.

<br>

    NOTE: If the user is not an admin, they can only use their own recipes and recipes that are public. If the user is an admin, they will be able to use any recipe to create a shopping list.

<br>

**Example Request**:
`/shopping-list?recipe_ids=1&recipe_ids=2&recipe_ids=3`

<br>

**Example Success Response**:

- 200 OK:
  
  ```json
  [
    {
      "ingredient_id": 1,
      "name": "Chicken Breast",
      "quantity": 750,
      "unit": "grams"
    },
    {
      "ingredient_id": 2,
      "name": "Rice",
      "quantity": 500,
      "unit": "grams"
    }
  ]
  ```

<br>

**Error Responses**:
  
- 400 Bad Request:

  ```json
  {
    "error": "Missing data",
    "message": "No recipes provided. Please include at least one recipe ID in the 'recipe_ids' query parameter."
  }
  ```

<br>

- 403 Forbidden:

  ```json
  {
    "error": "Access denied",
    "message": "One or more recipes not found or not accessible.",
    "details": "You don't have permission to access or the following recipe IDs do not exist: [4, 5]"
  }
  ```

<br>

- 500 Internal Server Error:

  ```json
  {
    "error": "An unexpected error occurred",
  }
  ```

<br>
<br>

### Search Routes:

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Search Recipes | `/search/recipes` | GET | JWT in header | `q` (search query string) |

<br>

    NOTE: If the user is not an admin, they can only search their own recipes and public recipes. If the user is an admin, they can search all recipes.

<br>

    NOTE: Searching for recipes will return recipes that match the search query string in the recipe name or description.

<br>

**Example Request**:
`/search/recipes?q=chicken`

<br>

**Example Success Response**:

- 200 OK:
  
  ```json
  {
    "recipes": [
      {
        "id": 1,
        "name": "Grilled Chicken",
        "description": "Juicy grilled chicken breast",
        "instructions": "1. Marinate chicken...",
        "is_public": true,
        "user_id": 2,
        "ingredients": [
          {
            "id": 1,
            "ingredient_id": 5,
            "name": "Chicken Breast",
            "quantity": 500,
            "unit": "grams"
          }
        ]
      }
    ]
  }
  ```

<br>

**Error Responses**:
  
- 400 Bad Request:

  ```json
  {
    "error": "Invalid search",
    "message": "Please provide a search query using the 'q' parameter."
  }
  ```

<br>

- 404 Not Found:

  ```json
  {
    "message": "No recipes found",
    "details": "Your search did not match any recipes. Try different keywords or check your permissions."
  }
  ```

<br>
<br>

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Search Ingredients | `/search/ingredients` | GET | None | `q` (search query string), `category` |

<br>

    NOTE: Searching for ingredients will return ingredients that match the search query string. If category is provided, the search will only return ingredients that match the category and search query string. If only the category is provided, the search will return all ingredients that match the category.

<br>

**Example Request**:
`/search/ingredients?q=broccoli&category=vegetable`

<br>

**Example Success Response**:

- 200 OK:
  
  ```json
  {
    "ingredients": [
        {
            "calories": 55.0,
            "carbohydrates": 11.2,
            "category": "Vegetable",
            "fat": 0.6,
            "fiber": null,
            "id": 3,
            "minerals": null,
            "name": "Broccoli",
            "protein": 3.7,
            "vitamins": null
        }
    ]
  }
  ```

<br>
<br>

---

<br>
<br>

| FUNCTION | PATH | METHOD | AUTH REQUIRED | QUERY PARAMETERS |
|----------|------|--------|----------------|------------------|
| Search Recipes by Ingredient | `/search/recipes/by_ingredient` | GET | JWT in header | `ingredient_id` |

<br>

    NOTE: Searching for recipes by ingredient will return all recipes that contain the specified ingredient.

<br>

    NOTE: If the user is not an admin, they can only search their own recipes and public recipes. If the user is an admin, they can search all recipes.

<br>

**Example Request**:
`/search/recipes/by_ingredient?ingredient_id=5`

<br>

**Example Success Response**:

- 200 OK:
  
  ```json
  {
    "recipes": [
      {
        "id": 1,
        "name": "Chicken Stir Fry",
        "description": "A quick and easy chicken stir fry recipe",
        "instructions": "1. Cut chicken into cubes...",
        "is_public": true,
        "user_id": 2,
        "ingredients": [
          {
            "id": 1,
            "ingredient_id": 5,
            "name": "Chicken Breast",
            "quantity": 500,
            "unit": "grams"
          },
          {
            "id": 2,
            "ingredient_id": 8,
            "name": "Soy Sauce",
            "quantity": 30,
            "unit": "ml"
          }
        ]
      },
      {
        "id": 3,
        "name": "Grilled Chicken Salad",
        "description": "A healthy and delicious grilled chicken salad",
        "instructions": "1. Grill chicken breast...",
        "is_public": true,
        "user_id": 1,
        "ingredients": [
          {
            "id": 7,
            "ingredient_id": 5,
            "name": "Chicken Breast",
            "quantity": 300,
            "unit": "grams"
          },
          {
            "id": 8,
            "ingredient_id": 12,
            "name": "Mixed Salad Greens",
            "quantity": 200,
            "unit": "grams"
          }
        ]
      },
      {
        "id": 5,
        "name": "Chicken Soup",
        "description": "A comforting chicken soup recipe",
        "instructions": "1. Boil chicken breast...",
        "is_public": true,
        "user_id": 2,
        "ingredients": [
          {
            "id": 13,
            "ingredient_id": 5,
            "name": "Chicken Breast",
            "quantity": 400,
            "unit": "grams"
          },
          {
            "id": 14,
            "ingredient_id": 15,
            "name": "Carrots",
            "quantity": 100,
            "unit": "grams"
          }
        ]
      }
    ]
  }
  ```

<br>

**Error Responses**:
  
- 400 Bad Request:

  ```json
  {
    "error": "Missing parameter",
    "message": "Ingredient ID is required. Please provide an 'ingredient_id' parameter in your request."
  }
  ```

  ```json
  {
    "error": "Invalid parameter",
    "message": "The provided ingredient_id must be a valid integer."
  }
  ```

<br>

- 404 Not Found:

  ```json
  {
    "message": "No recipes found",
    "details": "No recipes were found with the specified ingredient. This could be because the ingredient doesn't exist, or you don't have permission to view recipes using this ingredient."
  }
  ```

<br>
<br>

---














<style>
    table {
        width: 100%;
    }
</style>