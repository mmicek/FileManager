#!/bin/bash
set -e

export PYTHONPATH=$PYTHONPATH:/app

poetry run python file_manager/manage.py migrate
poetry run python file_manager/manage.py collectstatic --noinput
poetry run python file_manager/manage.py runserver 0.0.0.0:8000
