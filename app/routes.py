from flask import Blueprint, render_template, request, jsonify
from .utils import (
    save_face_encoding,
    find_matching_face,
    save_face_data,
)
import os
from datetime import datetime

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["image"]
    url = request.form.get("url")
    reason = request.form.get("reason")

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not url:
        return jsonify({"error": "URL is required"}), 400

    if not reason:
        return jsonify({"error": "Reason is required"}), 400

    # Check if face already exists
    temp_path = save_face_encoding(file)
    if not temp_path:
        return jsonify({"error": "Could not process the image"}), 400

    # Check if face already exists in database
    if find_matching_face(temp_path):
        os.remove(temp_path)  # Clean up temporary file
        return jsonify({"error": "Face already registered in system"}), 400

    # Save the face data
    face_data = {
        "url": url,
        "reason": reason,
        "encoding_path": temp_path,
        "timestamp": datetime.now().isoformat(),
    }

    # Save to database (you'll need to implement this)
    save_face_data(face_data)

    return jsonify({"success": True, "message": "Face registered successfully"})


@bp.route("/verify", methods=["POST"])
def verify():
    if "image" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save the verification image temporarily
    temp_path = save_face_encoding(file)
    if not temp_path:
        return jsonify({"error": "Could not process the image"}), 400

    # Get match and associated data
    match_data = find_matching_face(temp_path)

    # Clean up temporary file
    os.remove(temp_path)

    if match_data:
        return jsonify(
            {
                "match": True,
                "data": {
                    "url": match_data["url"],
                    "reason": match_data["reason"],
                    "timestamp": match_data["timestamp"],
                },
            }
        )

    return jsonify({"match": False})
