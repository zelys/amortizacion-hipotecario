import pandas as pd
from fpdf import FPDF
import io
import requests

# Obtener el valor actual de la UF
def obtener_valor_uf():
    url = "https://www.mindicador.cl/api/uf/"
    respuesta = requests.get(url)
    data = respuesta.json()
    return data['serie'][0]['valor']



# Calcular la tabla de amortización
def tabla_amort_en_uf(valor_propiedad, porc_financ,tasa_anual, plazo_anos):

    prestamo_uf = valor_propiedad * (porc_financ / 100)

    tasa_mensual = (tasa_anual / 100) / 12
    n_meses = plazo_anos * 12
    cuota = (prestamo_uf * tasa_mensual) / (1 - (1 + tasa_mensual) ** -n_meses)
    saldo = prestamo_uf
    filas = []
    for mes in range(1, n_meses + 1):
        interes = saldo * tasa_mensual
        amort = cuota - interes
        saldo -= amort
        filas.append([
            str(mes),
            float(cuota), 
            float(interes),
            float(amort), 
            float(max(saldo, 0)),
        ])
    df = pd.DataFrame(filas, columns=["Mes", "Cuota", "Interés", "Amortización", "Saldo"])
    return df

# Calcular la tabla de amortización en CLP
def tabla_amortizacion_en_clp(valor_propiedad, porc_financ, tasa_anual, plazo_anos):
    valor_uf = obtener_valor_uf()
    df_uf = tabla_amort_en_uf(valor_propiedad, porc_financ, tasa_anual, plazo_anos)
    df_clp = df_uf.copy()
    df_clp["Cuota"] = df_clp["Cuota"] * valor_uf
    df_clp["Interés"] = df_clp["Interés"] * valor_uf
    df_clp["Amortización"] = df_clp["Amortización"] * valor_uf
    df_clp["Saldo"] = df_clp["Saldo"] * valor_uf
    return df_clp

# Exportar tablas a diferentes formatos
def exportar_excel(tabla):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        tabla.to_excel(writer, index=False)
    output.seek(0)
    return output

# Exportar tabla a CSV
def exportar_csv(tabla):
    output = io.StringIO()
    tabla.to_csv(output, index=False, encoding='utf-8')
    output.seek(0)
    return output

# Exportar tabla a PDF
def exportar_pdf(tabla):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    # Añadir título
    pdf.cell(0, 10, 'Tabla de Amortización en UF', ln=True, align='C')
    col_width = pdf.w / (len(tabla.columns) + 1)
    row_height = pdf.font_size * 1.5
    for col in tabla.columns:
        pdf.cell(col_width, row_height, str(col), border=1, align='C')
    pdf.ln(row_height)
    pdf.set_font('Arial', '', 10)
    for _, row in tabla.iterrows():
        for item in row:
            pdf.cell(col_width, row_height, str(item), border=1)
        pdf.ln(row_height)
    output = io.BytesIO(pdf.output(dest='S').encode('latin1'))
    output.seek(0)
    return output                   

# Formatear datos a 2 decimales
def formatear_dataframe(df):
    df_formateado = df.copy()
    for col in df_formateado.columns:
        if col != "Mes":
            df_formateado[col] = df_formateado[col].apply(lambda x: f"{x:.2f}")
    return df_formateado  
