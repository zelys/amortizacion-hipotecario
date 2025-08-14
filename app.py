from flask import Flask, render_template, request, send_file
from utils import calcular_tabla_amortizacion, exportar_excel, exportar_pdf

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    tabla = None
    if request.method == 'POST':
        valor = float(request.form['valor'])
        porcentaje = float(request.form['porcentaje'])
        tasa = float(request.form['tasa'])
        plazo = int(request.form['plazo'])
        tabla = calcular_tabla_amortizacion(valor, porcentaje, tasa, plazo)
    return render_template('index.html', tabla=tabla)

@app.route('/descargar/<formato>', methods=['POST'])
def descargar(formato):
    valor = float(request.form['valor'])
    porcentaje = float(request.form['porcentaje'])
    tasa = float(request.form['tasa'])
    plazo = int(request.form['plazo'])
    tabla = calcular_tabla_amortizacion(valor, porcentaje, tasa, plazo)
    if formato == 'excel':
        output = exportar_excel(tabla)
        return send_file(output, as_attachment=True, download_name='amortizacion.xlsx')
    elif formato == 'pdf':
        output = exportar_pdf(tabla)
        return send_file(output, as_attachment=True, download_name='amortizacion.pdf')
    else:
        return 'Formato no soportado', 400

if __name__ == '__main__':
    app.run(debug=True)