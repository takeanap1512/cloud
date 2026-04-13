from flask import Flask, request, jsonify
from google.cloud import storage
import time

app = Flask(__name__)

client = storage.Client()
bucket = client.bucket("your-bucket-name")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]

    filename = str(int(time.time())) + "_" + file.filename
    blob = bucket.blob(filename)

    blob.upload_from_file(file)

    url = blob.generate_signed_url(expiration=3600)

    return jsonify({
        "message": "Upload successful",
        "url": url
    })

@app.route("/files", methods=["GET"])
def list_files():
    blobs = bucket.list_blobs()

    files = []
    for blob in blobs:
        url = blob.generate_signed_url(expiration=3600)

        files.append({
            "name": blob.name,
            "url": url,
            "isImage": blob.name.endswith(("png", "jpg", "jpeg"))
        })

    return jsonify(files)

if __name__ == "__main__":
    app.run()