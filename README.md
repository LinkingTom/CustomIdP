# Lightweight IDP

A lightweight identity provider service built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- FastAPI web framework with automatic API documentation
- SQLAlchemy ORM with PostgreSQL support
- Alembic database migrations
- User model with email, name, roles, and teams
- Email uniqueness enforcement at database level
- Health check endpoint

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Virtual environment (venv)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd lightweight-idp
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp config.env.template .env
   # Edit .env file with your database credentials
   ```

5. **Set up the database:**
   - Create a PostgreSQL database named `lightweight_idp`
   - Update the `DATABASE_URL` in your `.env` file if needed

6. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

## Running the Application

Start the development server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at:
- Main application: http://localhost:8000
- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Project Structure

```
lightweight-idp/
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   └── config.py          # Database configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py            # User model
│   └── __init__.py
├── alembic/
│   ├── versions/              # Migration files
│   ├── env.py                 # Alembic environment
│   └── ...
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── alembic.ini               # Alembic configuration
├── config.env.template       # Environment variables template
└── .env                      # Environment variables (create from template)
```

## Database Schema

### Users Table

- `id`: Primary key (Integer)
- `email`: Unique email address (String) - automatically converted to lowercase
- `name`: User's full name (String)
- `roles`: List of user roles (JSON array)
- `teams`: List of teams user belongs to (JSON array)
- `created_at`: Timestamp when user was created
- `updated_at`: Timestamp when user was last updated

## Development

### Creating New Migrations

After modifying models, create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

### Environment Variables

Key environment variables (see `config.env.template`):
- `DATABASE_URL`: PostgreSQL connection string
- `DEBUG`: Enable debug mode
- `SECRET_KEY`: Secret key for the application

## API Endpoints

### Core Endpoints
- `GET /`: Root endpoint with API information
- `GET /health`: Health check endpoint
- `GET /docs`: Swagger UI documentation
- `GET /redoc`: ReDoc documentation

### User Endpoints
- `POST /users`: Create a new user
- `GET /users`: List all users (with pagination)
- `GET /users/{email}`: Get a user by email (case-insensitive)
- `PUT /users/{email}`: Replace a user completely
- `PATCH /users/{email}`: Update specific user fields
- `DELETE /users/{email}`: Delete a user

### Team Endpoints (Optional)
- `POST /teams`: Create a new team
- `GET /teams`: List all teams (with pagination)
- `GET /teams/{team_id}`: Get a team by ID
- `PUT /teams/{team_id}`: Replace a team completely
- `DELETE /teams/{team_id}`: Delete a team

### Features
- ✅ **Email normalization**: All emails automatically converted to lowercase
- ✅ **Case-insensitive lookups**: Find users by email regardless of case
- ✅ **Unique email enforcement**: Database-level uniqueness with `LOWER(email)` index
- ✅ **Input validation**: Pydantic schemas with proper email validation
- ✅ **Error handling**: Comprehensive HTTP error responses
- ✅ **Pagination**: Support for `skip` and `limit` parameters
- ✅ **JSON arrays**: Roles and teams stored as JSON arrays

## Testing the API

### Using the Demo Script
```bash
# Start the server
python main.py

# In another terminal, run the demo
python demo_api.py
```

### Manual Testing Examples
```bash
# Create a user
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "john.DOE@example.com",
       "name": "John Doe",
       "roles": ["admin", "user"],
       "teams": ["engineering"]
     }'

# Get user (case-insensitive)
curl "http://localhost:8000/users/JOHN.DOE@EXAMPLE.COM"

# Update user roles
curl -X PATCH "http://localhost:8000/users/john.doe@example.com" \
     -H "Content-Type: application/json" \
     -d '{"roles": ["admin", "super-user"]}'

# List all users
curl "http://localhost:8000/users"

# Create a team
curl -X POST "http://localhost:8000/teams" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Engineering",
       "description": "Software development team",
       "user_emails": ["john.doe@example.com"]
     }'
``` 