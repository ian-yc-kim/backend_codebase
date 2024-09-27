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

## Best Practices

- **Environment Variables**: Use environment variables to manage sensitive information such as database credentials and API keys.

- **Error Handling**: Implement robust error handling in your API calls to ensure smooth user experience.

- **Testing**: Regularly run unit tests to ensure the integrity of the backend services. Use the `pytest` framework for testing.

- **Code Quality**: Follow Python best practices and PEP 8 guidelines to maintain code quality and readability.

This README provides a comprehensive guide to setting up and using the backend subsystem of the Dynamic Novel Generator project. For further details, refer to the design documentation linked in the project repository.