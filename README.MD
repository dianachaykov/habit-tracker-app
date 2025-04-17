# HabitEasy

A command-line habit tracking application with a backend API, built using Python, Flask, and SQLAlchemy.

## Overview

HabitEasy provides a simple and efficient way to create, track, and analyze your habits through an intuitive command-line interface (CLI). It allows you to define habits with different frequencies (daily, weekly), record completions, and monitor your progress using streak tracking. The application also includes a Flask-based backend API for potential future expansion and internal data management.

## Technologies Used

* **Python:** The core programming language.
* **Flask:** A micro web framework for the backend API.
* **SQLAlchemy:** An SQL toolkit and Object Relational Mapper (ORM) for database interaction.
* **PostgreSQL:** The relational database used to store application data.
* **Flask-Migrate:** An extension for handling database schema migrations.

## How to Use

### Prerequisites

Ensure you have Python 3.6 or higher installed on your system.

### Installation

1.  Clone the repository to your local machine:
    ```bash
    git clone <https://github.com/dianachaykov/habit-tracker-app>
    cd habit_tracker_app
    ```
   

2.  It's recommended to create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # venv\Scripts\activate   # On Windows
    ```

3.  Install the required dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```
   

4.  Initialize database migrations (if not done already):
    ```bash
    flask db init
    ```

5.  Create the initial migration:
    ```bash
    flask db migrate -m "Initial migration"
    ```

6.  Apply the migrations to create the database schema:
    ```bash
    flask db upgrade
    ```

### Running the Application

1.  **Running the Backend API (Optional):**
    To run the Flask-based backend API, navigate to the project root directory and execute:
    ```bash
    python app.py
    ```
    The API will be accessible at `http://127.0.0.1:5000`.

2.  **Using the Command-Line Interface (CLI):**
    Navigate to the project root directory and run the CLI using the Python interpreter:
    ```bash
    python cli.py <command> [options]
    ```

### Basic CLI Commands

* **Register a new user:**
    ```bash
    python cli.py register
    ```
* **Log in to your account:**
    ```bash
    python cli.py login
    ```
* **Create a new habit:**
    ```bash
    python cli.py create --name "Read for 30 minutes" --frequency daily --description "Daily reading habit"
    python cli.py create --name "Go for a run" --frequency weekly --description "Run at least once a week"
    ```
* **List all habits (optionally filter by frequency):**
    ```bash
    python cli.py list
    python cli.py list --frequency daily
    python cli.py list --frequency weekly
    ```
* **Mark a habit as complete (optionally specify the date):**
    ```bash
    python cli.py complete --name "Read for 30 minutes"
    python cli.py complete --name "Go for a run" --on 2025-04-20
    ```
* **Check your current and longest streaks (optionally for a specific habit or all):**
    ```bash
    python cli.py streak --name "Read for 30 minutes"
    python cli.py streak --all
    ```

## Project Structure
habit_tracker_app/
├── .venv/          # Virtual environment directory 
├── migrations/     # Directory containing database migration files
│   └── versions/   # Contains the actual migration scripts
├── tests/          # Directory for unit tests
│   ├── test_models.py
│   ├── test_routes.py
│   ├── test_app.py
│   └── ...
├── app.py          # Main Flask application (backend API)
├── cli.py          # Command-line interface logic
├── extensions.py   # Flask extensions initialization
├── models.py       # Database models (SQLAlchemy)
├── passwords.txt   # Potentially for initial user setup 
├── README.md       # This file
├── routes.py       # API routes for the backend
├── utils.py        # Utility functions 
├── requirements.txt# Lists the project dependencies
└── ... (other files)

## Documentation

The code itself is documented with basic comments to aid understanding and maintainability.

## Author

Diana Ceaicovschi
