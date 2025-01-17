from .models import SQLWatchlistPerson
from datetime import datetime
import numpy as np
import face_recognition
import os
from werkzeug.utils import secure_filename
from . import get_db

UPLOAD_FOLDER = "app/uploads"


def save_face_data(face_data):
    """Save face data to PostgreSQL database"""
    db = get_db()
    person = db.WatchlistPerson(
        source_url=face_data["url"],
        reason=face_data["reason"],
        image_path=face_data["encoding_path"],
    )

    try:
        db.add(person)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error saving to database: {str(e)}")
        raise


def find_matching_face(verify_encoding_path):
    """Find matching face and return associated data from database"""
    db = get_db()
    try:
        verify_encoding = np.load(verify_encoding_path)

        # Get all persons from database
        all_persons = db.query_all(db.WatchlistPerson)

        # Compare with each stored encoding
        for person in all_persons:
            if os.path.exists(person.image_path):
                known_encoding = np.load(person.image_path)
                match = face_recognition.compare_faces(
                    [known_encoding], verify_encoding, tolerance=0.6
                )[0]

                if match:
                    return {
                        "url": person.source_url,
                        "reason": person.reason,
                        "timestamp": person.created_at.isoformat(),
                    }

        return None

    except Exception as e:
        print(f"Error in face comparison: {str(e)}")
        return None


def save_face_encoding(file):
    """Save uploaded image and return path to its encoding"""
    try:
        # Create upload folder if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Get the filename and create paths
        filename = secure_filename(file.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        encoding_path = os.path.splitext(image_path)[0] + ".npy"

        # Save the uploaded file
        file.save(image_path)

        # Load the image and create encoding
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if not face_encodings:
            os.remove(image_path)
            return None

        # Save the encoding
        np.save(encoding_path, face_encodings[0])

        # Clean up the original image
        os.remove(image_path)

        return encoding_path

    except Exception as e:
        print(f"Error processing image: {str(e)}")
        # Clean up any files if there was an error
        if "image_path" in locals() and os.path.exists(image_path):
            os.remove(image_path)
        if "encoding_path" in locals() and os.path.exists(encoding_path):
            os.remove(encoding_path)
        return None
