# Feature Flag Service

## Overview
This project is a RESTful API designed to manage feature flags. It allows applications to dynamically enable or disable features across different environments (e.g., development, production) without redeploying code.

## Architecture
The application follows a standard layered architecture:

* **FastAPI**: The web framework that handles HTTP requests and routing.
* **SQLAlchemy**: The ORM (Object Relational Mapper) used to interact with the database using Python objects instead of raw SQL.
* **PostgreSQL**: The relational database used to store flag definitions and settings (configured via Docker).

## Project Structure
Understanding the files in this repository:

* **`main.py`**: The entry point of the application. It initializes the FastAPI app and defines the API endpoints (routes).
* **`database.py`**: Manages the database connection. It creates the "Engine" (connection pool) and the "SessionLocal" (factory for creating database sessions per request).
* **`models.py`**: Defines the database schema. It contains Python classes (inheriting from `Base`) that map directly to SQL tables (e.g., `Flag`, `FlagSetting`).
* **`requirements.txt`**: A list of all Python dependencies required to run the project.

## Database Schema
The database consists of two primary tables with a one-to-many relationship:

1.  **Flags (`flags`)**:
    * Stores the identity of the feature (name, description).
    * Acts as the parent record.

2.  **Flag Settings (`flag_settings`)**:
    * Stores the configuration for a flag in a specific environment.
    * Contains the `is_enabled` boolean switch.
    * Linked to the parent Flag via a Foreign Key.

## Setup Instructions (Local Development)

### 1. Environment Setup
Ensure you have Python 3 installed. Create a virtual environment to isolate dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
