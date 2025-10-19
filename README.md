# File Manager Backend

A Django-based file management backend with image handling, REST API endpoints, PostgreSQL database support and pytest. 

## Project setup

1. Create a .env file inside the file_manager directory and copy the content from .env.example.
2. Run docker compose up

For local development without Docker:
1. poetry install
2. python manage.py migrate
3. python manage.py runserver 
4. python manage.py createsuperuser

### Tests

1. Run pytest . inside file_manager package.
