from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Cargar datos desde el archivo JSON
def cargar_datos():
    with open('data/data.json') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

# ir al punto 1
@app.route('/punto1')
def punto1():
    return render_template('punto1.html')

@app.route('/regiones', methods=['GET'])
def regiones():
    datos = cargar_datos()
    regiones = [item['region'] for item in datos]
    return jsonify(regiones)

if __name__ == '__main__':
    app.run(debug=True)