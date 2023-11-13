from flask import Flask, request, render_template, redirect, url_for, send_file, jsonify
from PIL import Image
import os
from static import electre_four as ef
import json

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

@app.route('/electre_four')
def electre_four():
    return render_template("electre_four.html")

@app.route('/WPM_WSM')
def WPM_WSM():
    return render_template("WPM_WSM.html")

@app.route('/post_electre_four', methods=["POST"])
def post_electre_four():
    
    # csv_file = request.files['csv_file']
    
    # if request.files['csv_file']:
    #     csv_file = request.files['csv_file']
    # else:
    #     pass
    
    matrix = request.form.get('matrix')
    weight = request.form.get('weight')
    
    matrix = json.loads(matrix)
    weight = json.loads(weight)
    
    result = ef.initiation(matrix, weight)
    
    return jsonify({'message': 'success', 'result': result})

if __name__ == "__main__":
    app.run(debug=True)

