from flask import Flask, request, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

cloudinary.config(
    cloud_name = os.environ.get("CLOUD_NAME"),
    api_key = os.environ.get("API_KEY"),
    api_secret = os.environ.get("API_SECRET")
)


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    result = cloudinary.uploader.upload(file)

    return jsonify({
        "url": result["secure_url"]
    })


@app.route("/files", methods=["GET"])
def files():
    result = cloudinary.api.resources()

    files = []
    for r in result["resources"]:
        files.append({
            "name": r["public_id"],
            "url": r["secure_url"],
            "public_id": r["public_id"],
            "isImage": r["resource_type"] == "image"
        })

    return jsonify(files)


@app.route("/delete/<public_id>", methods=["DELETE"])
def delete_file(public_id):
    cloudinary.uploader.destroy(public_id)
    return jsonify({"message": "Deleted"})

if __name__ == "__main__":
    app.run()