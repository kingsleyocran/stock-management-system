# Stock Management System

Welcome to the Stock Management Application. This application is designed to help you efficiently manage your stock and inventory. This README provides essential information on how to set up and use the application.

## Table of Contents

- [Stock Management System](#stock-management-system)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [API Documentation](#api-documentation)
  - [Project Structure](#project-structure)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- User authentication and authorization.
- Create, update, and delete products.
- Track stock levels and inventory.
- Manage and process orders

## Prerequisites

Before setting up the Stock Management Application, ensure you have the following prerequisites:

- [Python 3.9+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://www.docker.com/) (optional, for running with Docker)
- [Git](https://git-scm.com/)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/stock-management-app.git
   cd stock-management-app
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Set up environment variables:

   Create a `.env` file in the root directory with the following content:

   ```
   DATABASE_URL=sqlite:///./stock.db
   SECRET_KEY=your_secret_key
   ```

   Replace `your_secret_key` with a strong secret key for securing your application.

4. Apply database migrations:

   ```bash
   poetry run alembic upgrade head
   ```

## Usage

1. Start the FastAPI server using Poetry:

   ```bash
   poetry run uvicorn main:app --host 0.0.0.0 --port 8000
   ```

   The server should now be running at `http://localhost:8000`.

2. Access the Stock Management Application in your web browser by navigating to `http://localhost:8000`.

3. Register a user or log in to an existing account.

4. Use the application to add, update, and manage your stock and inventory.

## API Documentation

The Stock Management Application provides a comprehensive API that you can use for integration with other systems. You can access the API documentation by navigating to `http://localhost:8000/docs` when the application is running.

## Project Structure

- `main.py`: FastAPI application entry point.
- `api`: Stock management endpoints.
- `models`: Database models.
- `migrations`: Database migration scripts.
- `alembic.ini`: Alembic configuration file for database migrations.
- `static`: Static files (e.g., images, CSS).
- `templates`: HTML templates (if applicable).
- `utils`: Database helper funtions and session class.
- `schema`: Pydantic schemas for models.
- `handlers`: Error handler definitions.
- `core`: FastAPI app configuration and initialization.
- `controller`: Controller functions for various use cases.
- `config`: App configurations.

## Contributing

Contributions to this project are welcome. Feel free to open issues and pull requests to help improve the Stock Management Application.

## License

This Stock Management Application is open-source software released under the [MIT License](LICENSE).