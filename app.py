from flask import Flask, render_template, request, send_file
from utils import tabla_amort_en_uf, exportar_excel, exportar_pdf, formatear_dataframe
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    tabla = None
    if request.method == 'POST':
        valor = float(request.form['valor'])
        porcentaje = float(request.form['porcentaje'])
        tasa = float(request.form['tasa'])
        plazo = int(request.form['plazo'])
        tabla = tabla_amort_en_uf(valor, porcentaje, tasa, plazo)
    return render_template('index.html', tabla=tabla)

# Route para descargar la tabla en diferentes formatos
@app.route('/descargar/<formato>', methods=['POST'])
def descargar(formato):
    valor = float(request.form['valor'])
    porcentaje = float(request.form['porcentaje'])
    tasa = float(request.form['tasa'])
    plazo = int(request.form['plazo'])
    tabla = tabla_amort_en_uf(valor, porcentaje, tasa, plazo)
    
    if formato == 'excel':
        output = exportar_excel(formatear_dataframe(tabla))
        return send_file(output, as_attachment=True, download_name='amortizacion.xlsx')
    elif formato == 'pdf':
        output = exportar_pdf(formatear_dataframe(tabla))
        return send_file(output, as_attachment=True, download_name='amortizacion.pdf')
    else:
        return 'Formato no soportado', 400

if __name__ == '__main__':
    app.run(debug=True)