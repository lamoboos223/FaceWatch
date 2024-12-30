import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your-secret-key-here"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql://facewatch:facewatch@localhost/facewatch"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "app/static/uploads"
    )
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
