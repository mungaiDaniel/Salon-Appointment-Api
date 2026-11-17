"""Production entrypoint: ``gunicorn wsgi:app``."""

from main import create_app

app = create_app()
