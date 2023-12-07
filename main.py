from flask import Flask, request, render_template, redirect, url_for, send_file, jsonify
from PIL import Image
import os
from static import electre_four as ef
import json
from static.caesar_cipher import caesar_encode, caesar_decode
import pandas as pd
import numpy as np

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

@app.route('/post_electre_four', methods=["POST"])
def post_electre_four():
    
    matrix = request.form.get('matrix')
    weight = request.form.get('weight')
    
    matrix = json.loads(matrix)
    weight = json.loads(weight)
    
    result = ef.initiation(matrix, weight)
    
    return jsonify({'message': 'success', 'result': result})

@app.route('/post_csv_electre', methods=["POST"])
def post_csv_electre():
        
    csv_file = request.files['csv_file']
    data = pd.read_csv(csv_file, header=None)
    
    if data.shape[1] == 1:
        data_temp = []
        
        for i in range(len(data)):
            data_split = str(data.iloc[i].values).replace('[', '').replace(']', '').strip("'").split(';')
            data_temp.append(data_split)

        data = pd.DataFrame(data_temp)
    
    if type(data[0][0]) == str:
        data = data.drop(0, axis=0)
    
    data_list = data.values.tolist()
    
    result = data_list
    
    return jsonify({'message': 'success', 'result': result})

@app.route('/Caesar_Cipher')
def view_caesar_cipher():
    return render_template("caesar_cipher.html")

@app.route('/Caesar_Cipher/result', methods=['POST'])
def result():
    if request.method == 'POST':
        text = request.form['inputText']
        shift = int(request.form['shiftAmount'])
        operation = request.form['operation']

        result_text = ''
        if operation == 'encode':
            result_text = caesar_encode(text, shift)
        elif operation == 'decode':
            result_text = caesar_decode(text, shift)

        return render_template('caesar_cipher.html', result=result_text)  
    
@app.route('/borda')
def view_borda():
    return render_template("borda.html")
if __name__ == "__main__":
    app.run(debug=True)

