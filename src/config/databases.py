import os

CONNECTIONS = {
    "default": {
        "DB_URI": os.getenv(
            "DB_URI", "mongodb://db_user:db_password@document-hub-mongodb:27017"
        ),
        "DB_NAME": os.getenv("DB_NAME", "documents"),
    }
}
