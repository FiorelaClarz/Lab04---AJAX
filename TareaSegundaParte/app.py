from flask import Flask, render_template, request, jsonify
import json
import os

# para visualizar la grafia del punto 5 se tuvo que hacer pip install de plotly en la terminal
import plotly.graph_objs as go

app = Flask(__name__)

# Cargar datos desde el archivo JSON
def cargar_datos():
    with open('data/data.json') as f:
        return json.load(f)

# Index donde se ve el desarrollo de cada punto del lab
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

# ir al punto 4
@app.route('/grafico_arequipa')
def grafico_arequipa():
    datos = cargar_datos()
    for region in datos:
        if region['region'] == 'Arequipa':
            fechas = [caso['date'] for caso in region['confirmed']]
            valores = [int(caso['value']) for caso in region['confirmed']]
            break
    return render_template('punto4.html', fechas=json.dumps(fechas), valores=json.dumps(valores))

# ir al punto 5
@app.route('/grafico_todas_regiones')
def mostrar_grafico_todas_regiones():
    grafico_html = grafico_todas_regiones()
    return render_template('punto5.html', grafico_html=grafico_html)

# ir al punto 6
@app.route('/grafico_todas_regiones_exceptoLimaCallao')
def mostrar_grafico_todas_regiones_exceptoLimaCallao():
    grafico_html = grafico_todas_regiones_exceptoLimaCallao()
    return render_template('punto6.html', grafico_html=grafico_html)

# ir al punto 7
@app.route('/comparar_regiones')
def comparar_regiones():
    return render_template('punto7.html')

# ir al punto 8
@app.route('/grafico_todas_regiones_exceptoLimaCallao8')
def mostrar_grafico_todas_regiones_exceptoLimaCallao8():
    grafico_html = grafico_todas_regiones_exceptoLimaCallao()
    return render_template('punto8.html', grafico_html=grafico_html)

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
                    top_10.pop()  
                    break

    # Ordenando top_10 en orden descendente usando el método de burbuja
    n = len(top_10)
    for i in range(n):
        for j in range(0, n-i-1):
            if top_10[j][1] < top_10[j+1][1]:
                top_10[j], top_10[j+1] = top_10[j+1], top_10[j]

    return top_10

# Función para generar el gráfico de líneas de todas las regiones
def grafico_todas_regiones():
    datos = cargar_datos()
    fechas = [entry['date'] for entry in datos[0]['confirmed']]  # Tomamos las fechas de la primera región
    regiones = [region['region'] for region in datos]
    datos_confirmados = {region['region']: [int(entry['value']) for entry in region['confirmed']] for region in datos}

    fig = go.Figure()

    for region, casos in datos_confirmados.items():
        fig.add_trace(go.Scatter(x=fechas, y=casos, mode='lines', name=region))

    fig.update_layout(title='Casos Confirmados por Región',
                      xaxis_title='Fecha',
                      yaxis_title='Casos Confirmados')

    return fig.to_html(full_html=False, include_plotlyjs='cdn')

# Función para generar el gráfico de líneas de todas las regiones
def grafico_todas_regiones_exceptoLimaCallao():
    datos = cargar_datos()
    fechas = [entry['date'] for entry in datos[0]['confirmed']]  # Tomamos las fechas de la primera región
    regiones = [region['region'] for region in datos]
    datos_confirmados = {region['region']: [int(entry['value']) for entry in region['confirmed']] for region in datos}

    fig = go.Figure()

    for region, casos in datos_confirmados.items():
        if region not in ["Lima", "Callao"]:
            fig.add_trace(go.Scatter(x=fechas, y=casos, mode='lines', name=region))

    fig.update_layout(title='Casos Confirmados por Región',
                      xaxis_title='Fecha',
                      yaxis_title='Casos Confirmados')

    return fig.to_html(full_html=False, include_plotlyjs='cdn')


# Funcion que permite visualizar la comparacion de los casos confirmados de dos regiones
@app.route('/graficar', methods=['POST'])
def graficar():
    datos = cargar_datos()
    region1 = request.json['region1']
    region2 = request.json['region2']

    region1_data = next(item for item in datos if item['region'] == region1)
    region2_data = next(item for item in datos if item['region'] == region2)

    fechas = []
    for data in region1_data['confirmed'] + region2_data['confirmed']:
        if data['date'] not in fechas:
            fechas.append(data['date'])
    fechas.sort()

    def preparar_datos(region_data):
        datos = {fecha: None for fecha in fechas}
        for data in region_data['confirmed']:
            datos[data['date']] = int(data['value'])
        return [datos[fecha] for fecha in fechas]

    region1_vals = preparar_datos(region1_data)
    region2_vals = preparar_datos(region2_data)

    datos_grafico = {
        "labels": fechas,
        "datasets": [
            {"label": region1, "data": region1_vals, "borderColor": '#'+format(int(os.urandom(1).hex(), 16)*111111, '06x'), "fill": False},
            {"label": region2, "data": region2_vals, "borderColor": '#'+format(int(os.urandom(1).hex(), 16)*111111, '06x'), "fill": False}
        ]
    }

    return jsonify(datos_grafico)

@app.route('/graficarTodasLasRegiones', methods=['POST'])
def graficarTodasLasRegiones():
    datos = cargar_datos()
    regiones = [item['region'] for item in datos if item['region'] not in ['Lima', 'Callao']]

    fechas = []
    for region_data in datos:
        for data in region_data['confirmed']:
            if data['date'] not in fechas:
                fechas.append(data['date'])
    fechas.sort()

    def preparar_datos(region_data):
        datos_preparados = {fecha: None for fecha in fechas}
        for data in region_data['confirmed']:
            datos_preparados[data['date']] = int(data['value'])
        return [datos_preparados[fecha] for fecha in fechas]

    datasets = []
    for region in regiones:
        region_data = next(item for item in datos if item['region'] == region)
        region_vals = preparar_datos(region_data)
        datasets.append({
            "label": region,
            "data": region_vals,
            "borderColor": '#' + format(int(os.urandom(1).hex(), 16) * 111111, '06x'),
            "fill": False
        })

    datos_grafico = {
        "labels": fechas,
        "datasets": datasets
    }

    return jsonify(datos_grafico)


if __name__ == '__main__':
    app.run(debug=True)