# HabitEase

A command-line habit tracking application built with Python, Flask, and SQLAlchemy.

## Overview

HabitEase allows users to create, track, and analyze their habits through a simple command-line interface. It provides features for defining habits with different frequencies (daily, weekly), recording completions, and viewing progress through streak tracking.

## Technologies Used

* Python
* Flask (for the web API)
* SQLAlchemy (for database management)
* [Mention your CLI interaction method]
* PostgreSQL (for the database)
* Flask-Migrate (for database migrations)
* pytest (for testing)

## How to Use

1.  **Prerequisites:** Ensure you have Python installed.
2.  **Running the CLI:** Navigate to the directory containing `habitease_cli.py` and run `python habitease_cli.py`.
3.  **Basic Commands:**
    * `create --name <habit_name> --frequency <daily|weekly> [--description <description>]` - Create a new habit.
    * `list [--frequency <daily|weekly>]` - List all habits (or filter by frequency).
    * `complete --name <habit_name> [--on <YYYY-MM-DD>]` - Mark a habit as complete.
    * `streak [--name <habit_name>|--all]` - Check your current and longest streaks.
    * `register` - Register a new user.
    * `login` - Log in to your account.

## Backend API

The application also includes a Flask-based backend API running at `http://127.0.0.1:5000` (when the `app.py` is running). It provides endpoints for user authentication, habit management, and retrieving analytics.

## Documentation

The code itself is documented with comments.

## Author

Diana
