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


@app.route('/post_borda', methods=['POST'])
def post_borda():
    data = request.json
    initial_matrix = data['initialMatrix']
    weight_matrix = data['weightMatrix']

    # Panggil fungsi untuk mengalikan matriks
    result = multiply_matrices(initial_matrix, weight_matrix)

    if result is None:
        return jsonify({"error": "Ukuran matriks tidak cocok"}), 400

    # Contoh respons balik ke klien (JavaScript) dengan hasil perhitungan
    return jsonify({"message": "Data diterima dan disimpan di server.", "result": result})


def multiply_matrices(initial_matrix, weight_matrix):
    result_matrix = []

    # Pastikan ukuran initial_matrix dan weight_matrix sama
    if len(initial_matrix) != len(weight_matrix):
        return None  # Atau sesuaikan dengan penanganan error yang sesuai

    for i in range(len(initial_matrix)):
        row_result = []
        for j in range(len(initial_matrix[i])):
            multiplied_value = initial_matrix[i][j] * weight_matrix[j]
            row_result.append(multiplied_value)
        result_matrix.append(row_result)

    return result_matrix

@app.route('/copeland')
def view_borda():
    return render_template("copeland.html")

if __name__ == "__main__":
    app.run(debug=True)

