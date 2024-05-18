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
@app.route('/total_confirmados')
def totales_por_region(): 
    totales = sumar_valores_por_region()
    return render_template('punto2.html', totales=totales)

# ir al punto 3
@app.route('/top_region')
def top_totales_por_region(): 
    top_totales = top_10_regiones()
    return render_template('punto3.html', totales=top_totales)

# Regiones
@app.route('/regiones', methods=['GET'])
def regiones():
    datos = cargar_datos()
    regiones = [item['region'] for item in datos]
    return jsonify(regiones)

# Función para sumar los valores de casos confirmados por región
def sumar_valores_por_region():
    datos = cargar_datos()
    totales_por_region = {}
    for region in datos:
        nombre_region = region['region']
        total_confirmados = sum(int(caso['value']) for caso in region['confirmed'])
        totales_por_region[nombre_region] = total_confirmados
    return totales_por_region

# Obtener las 10 regiones con mayores casos confirmados 
def top_10_regiones():
    def sumar_valores_por_region2():
        datos = cargar_datos()
        totales_por_region = []
        for region in datos:
            nombre_region = region['region']
            total_confirmados = sum(int(caso['value']) for caso in region['confirmed'])
            totales_por_region.append((nombre_region, total_confirmados))
        return totales_por_region

    totales_por_region = sumar_valores_por_region2()
    top_10 = []

    for region in totales_por_region:
        if len(top_10) < 10:
            top_10.append(region)
        else:
            for i in range(10):
                if region[1] > top_10[i][1]:
                    top_10.insert(i, region)
                    top_10.pop()  # Mantener el tamaño de top_10 en 10 elementos
                    break

    # Ordenando top_10 en orden descendente usando el método de burbuja
    n = len(top_10)
    for i in range(n):
        for j in range(0, n-i-1):
            if top_10[j][1] < top_10[j+1][1]:
                top_10[j], top_10[j+1] = top_10[j+1], top_10[j]

    return top_10


if __name__ == '__main__':
    app.run(debug=True)