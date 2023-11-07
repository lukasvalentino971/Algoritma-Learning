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

@app.route('/post_electre_four', methods=["POST"])
def post_electre_four():
    matrix = request.form.get('matrix')
    weight = request.form.get('weight')
    
    matrix = json.loads(matrix)
    weight = json.loads(weight)
    
    electre_four = ef.ElectreFour(matrix, weight)
    
    normalized_matrix = electre_four.normalized_matrix.toList()
    weighted_matrix = electre_four.weighted_matrix.toList()
    concordance_set = electre_four.concordance_set
    discordance_set = electre_four.discordance_set
    concordance_matrix = electre_four.concordance_matrix.toList()
    discordance_matrix = electre_four.discordance_matrix.toList()
    dominance_concordance_matrix = electre_four.dominance_concordance_matrix.toList()
    dominance_discordance_matrix = electre_four.dominance_discordance_matrix.toList()
    aggregate_dominance_matrix = electre_four.aggregate_dominance_matrix.toList()
    eliminated_alternative = electre_four.eliminated_alternative
    aggregate_list = electre_four.aggregate_list
    aggregate_rank = electre_four.aggregate_rank
    eliminate_rank = electre_four.eliminate_rank
    
    result = {
        'normalized_matrix': normalized_matrix,
        'weighted_matrix': weighted_matrix,
        'concordance_set': concordance_set,
        'discordance_set': discordance_set,
        'concordance_matrix': concordance_matrix,
        'discordance_matrix': discordance_matrix,
        'dominance_concordance_matrix': dominance_concordance_matrix,
        'dominance_discordance_matrix': dominance_discordance_matrix,
        'aggregate_dominance_matrix': aggregate_dominance_matrix,
        'eliminated_alternative': eliminated_alternative,
        'aggregate_list': aggregate_list,
        'aggregate_rank': aggregate_rank,
        'eliminate_rank': eliminate_rank
    }
    
    return jsonify({'message': 'success', 'result': result})

if __name__ == "__main__":
    app.run(debug=True)

