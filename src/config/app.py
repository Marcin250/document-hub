import os

APP_NAME = os.getenv("APP_NAME", "documents-hub-local")
ENV = os.getenv("ENV", "local")
SECRET_KEY = os.getenv("SECRET_KEY", "local")
DEBUG = os.getenv("DEBUG", "false").strip().lower() == "true"
