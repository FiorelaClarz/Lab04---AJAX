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

# ir al punto 2
# @app.route('/punto2')
# def punto2():
#     return render_template('punto2.html')

@app.route('/total_confirmados')
# def total_confirmados(): 
#     total = sumar_valores_confirmados()
#     return render_template('punto2.html', total=total)
# @app.route('/totales_por_region')
def totales_por_region(): 
    totales = sumar_valores_por_region()
    # general += sumar_valores_confirmados()
    return render_template('punto2.html', totales=totales)

# PUNTO 1
@app.route('/regiones', methods=['GET'])
def regiones():
    datos = cargar_datos()
    regiones = [item['region'] for item in datos]
    return jsonify(regiones)


# PUNTO 2
# Nueva función para sumar los valores de casos confirmados
def sumar_valores_confirmados():
    datos = cargar_datos()
    total_confirmados = 0
    for region in datos:
        for caso in region['confirmed']:
            total_confirmados += int(caso['value'])
    return total_confirmados

# Nueva función para sumar los valores de casos confirmados por región
def sumar_valores_por_region():
    datos = cargar_datos()
    totales_por_region = {}
    for region in datos:
        nombre_region = region['region']
        total_confirmados = sum(int(caso['value']) for caso in region['confirmed'])
        totales_por_region[nombre_region] = total_confirmados
    return totales_por_region



if __name__ == '__main__':
    app.run(debug=True)