from flask import Flask, render_template, request, send_file, redirect, url_for
from utils import tabla_amort_en_uf, tabla_amortizacion_en_clp, exportar_excel, exportar_pdf, formatear_dataframe, obtener_valor_uf
from datetime import datetime
import locale

# Configurar la localización para fechas en español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Para sistemas Linux/Unix/Mac
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Para Windows
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'es_CL.UTF-8')  # Para Chile específicamente
        except locale.Error:
            # Si no encuentra ninguna localización española, usar la predeterminada
            pass

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    tabla = None
    valor_uf = obtener_valor_uf()
    
    # Formatear la fecha usando la configuración de localización
    fecha = datetime.now()
    fecha_actual = fecha.strftime('%A, %d de %B de %Y').capitalize()
    
    if request.method == 'POST':
        valor = float(request.form['valor'])
        porcentaje = float(request.form['porcentaje'])
        tasa = float(request.form['tasa'])
        plazo = int(request.form['plazo'])
        tipo_moneda = request.form.get('tipo_moneda', 'uf')
        
        if tipo_moneda == 'clp':
            tabla = tabla_amortizacion_en_clp(valor, porcentaje, tasa, plazo)
        else:
            tabla = tabla_amort_en_uf(valor, porcentaje, tasa, plazo)
            
    return render_template('index.html', tabla=tabla, valor_uf=valor_uf, fecha_actual=fecha_actual, year=fecha.year)

# Ruta para nuevo cálculo - redirecciona al inicio
@app.route('/nuevo-calculo', methods=['GET'])
def nuevo_calculo():
    return redirect(url_for('index'))

# Route para descargar la tabla en diferentes formatos
@app.route('/descargar/<formato>', methods=['POST'])
def descargar(formato):
    valor = float(request.form['valor'])
    porcentaje = float(request.form['porcentaje'])
    tasa = float(request.form['tasa'])
    plazo = int(request.form['plazo'])
    tipo_moneda = request.form.get('tipo_moneda', 'uf')
    
    if tipo_moneda == 'clp':
        tabla = tabla_amortizacion_en_clp(valor, porcentaje, tasa, plazo)
        sufijo_moneda = '_clp'
    else:
        tabla = tabla_amort_en_uf(valor, porcentaje, tasa, plazo)
        sufijo_moneda = '_uf'
    
    if formato == 'excel':
        output = exportar_excel(formatear_dataframe(tabla))
        return send_file(output, as_attachment=True, download_name=f'amortizacion{sufijo_moneda}.xlsx')
    elif formato == 'pdf':
        output = exportar_pdf(formatear_dataframe(tabla))
        return send_file(output, as_attachment=True, download_name=f'amortizacion{sufijo_moneda}.pdf')
    else:
        return 'Formato no soportado', 400

if __name__ == '__main__':
    app.run()