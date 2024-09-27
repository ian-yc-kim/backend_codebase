# Dynamic Novel Generator - Backend Subsystem

## Overview
The Dynamic Novel Generator is a project designed to facilitate the creation of novels through dynamic user interactions and AI-driven content generation. The backend subsystem is responsible for handling user inputs, interacting with the AI model, and managing the iterative development of the novel. It includes API endpoints for user interactions and content generation.

## Installation Instructions

To set up the backend subsystem, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ian-yc-kim/backend_codebase.git
   cd backend_codebase
   ```

2. **Install Dependencies**
   Ensure you have Python installed. Then, install the required packages using Poetry:
   ```bash
   poetry install
   ```

3. **Configure the Database**
   Update the database configuration in `config.py` to match your setup. The default configuration is set to connect to a PostgreSQL database.

   ### Example Configuration
   In the `config.py` file, you will find a class `TestConfig` which is used for testing purposes. For production, you should create a similar configuration class, for example, `ProductionConfig`, and set the `SQLALCHEMY_DATABASE_URI` to your PostgreSQL database URI.

   ```python
   class ProductionConfig:
       SQLALCHEMY_DATABASE_URI = 'postgresql://backend_database:74171843-ff5b@10.138.0.4:5432/backend_database'
       SQLALCHEMY_TRACK_MODIFICATIONS = False
       SECRET_KEY = 'your_production_secret_key'
   ```

   - **SQLALCHEMY_DATABASE_URI**: This is the URI for your PostgreSQL database. It includes the username, password, host, port, and database name.
   - **SQLALCHEMY_TRACK_MODIFICATIONS**: Set this to `False` to disable the modification tracking system, which is unnecessary and can add overhead.
   - **SECRET_KEY**: A secret key for your application, used for session management and other security-related needs. Ensure this is kept secret and not hard-coded in production.

4. **Run Migrations**
   Apply database migrations to set up the necessary tables:
   ```bash
   alembic upgrade head
   ```

5. **Start the Backend Server**
   Run the server using:
   ```bash
   poetry run python src/backend_codebase/main.py
   ```

## Usage Guidelines

- **API Endpoints**: The backend provides several API endpoints for user interactions and content generation. Refer to the `views.py` file for detailed information on available endpoints and their usage.

- **User Authentication**: The system supports a login and signup mechanism. Ensure you have registered users before attempting to access protected endpoints.

## Examples

Here are some examples of how to interact with the API endpoints:

### Example 1: User Registration

**Request**:
```http
POST /api/register
Content-Type: application/json

{
  "username": "newuser",
  "password": "securepassword"
}
```

**Response**:
```json
{
  "message": "User registered successfully."
}
```

### Example 2: User Login

**Request**:
```http
POST /api/login
Content-Type: application/json

{
  "username": "newuser",
  "password": "securepassword"
}
```

**Response**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Example 3: Generate Content

**Request**:
```http
POST /api/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "prompt": "Once upon a time..."
}
```

**Response**:
```json
{
  "content": "Once upon a time, in a land far away, there was a..."
}
```

These examples demonstrate how to use the API for user registration, login, and content generation. Ensure you replace `<token>` with the actual token received from the login response.

## Best Practices

- **Environment Variables**: Use environment variables to manage sensitive information such as database credentials and API keys.

- **Error Handling**: Implement robust error handling in your API calls to ensure smooth user experience.

- **Testing**: Regularly run unit tests to ensure the integrity of the backend services. Use the `pytest` framework for testing.

- **Code Quality**: Follow Python best practices and PEP 8 guidelines to maintain code quality and readability.

This README provides a comprehensive guide to setting up and using the backend subsystem of the Dynamic Novel Generator project. For further details, refer to the design documentation linked in the project repository.
