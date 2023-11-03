from flask import Flask, request, render_template, redirect, url_for, send_file
from PIL import Image
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/png_to_jpg', methods=["GET", "POST"])
def png_to_jpg():
    converted = False
    if request.method == "POST":
        file = request.files["image"]
        if file and file.filename != "":
            img = Image.open(file)
            img = img.convert("RGB")  # Convert to RGB format
            img.save("static/images/output.jpg", "JPEG")
            converted = True
    return render_template('png_to_jpg.html', converted=converted)

@app.route('/download_image')
def download_image():
    return send_file('static/images/output.jpg', as_attachment=True)
if __name__ == "__main__":
    app.run(debug=True)

