# File Manager Backend

A Django-based file management backend with image handling, REST API endpoints, PostgreSQL database support and pytest. 

## Project setup

1. Run docker compose up (--build)

For local development without Docker:
1. Create a .env file inside the file_manager package and copy the content from .env.example.
2. poetry install
3. python manage.py migrate
4. python manage.py runserver 
5. python manage.py createsuperuser

### Tests

1. Run pytest . inside file_manager package.
