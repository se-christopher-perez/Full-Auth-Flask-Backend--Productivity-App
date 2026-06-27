# Full-Auth-Flask-Backend--Productivity-App

## Project Description

- Full authentication

- A user-owned resource (e.g., notes, journal entries, workouts, expenses, tasks)

- CRUD endpoints and pagination

- Secure access controls so users cannot view or edit each other’s data

## Installation

- git clone 

- cd server

- pipenv install

- pipenv shell

- flask db upgrade

- python seed.py

## Tools and Resources

- Python 3.10+

- Text Editor or IDE (e.g., VS Code)

- Git + GitHub

### Pipenv: The following Python packages:

- flask = "2.2.2"

- flask-sqlalchemy = "3.0.3"

- Werkzeug = "2.2.2"

- marshmallow = "3.20.1"

- faker = "15.3.2"

- flask-migrate = "4.0.0"

- flask-restful = "0.3.9"

- importlib-metadata = "6.0.0"

- importlib-resources = "5.10.0"

- pytest = "7.2.0"

- flask-bcrypt = "1.0.1"

## Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /signup | Register a new user |
| POST | /login | Login with username and password |
| DELETE | /logout | Logout current user |
| GET | /check_session | Check if user is logged in |

### Journal Entries
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /journal_entries | Get all entries for logged in user (paginated) |
| POST | /journal_entries | Create a new journal entry |
| PATCH | /journal_entries/<id> | Update a journal entry |
| DELETE | /journal_entries/<id> | Delete a journal entry |