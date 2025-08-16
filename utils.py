import pandas as pd
from doc_pdf import PDF
import io, os, requests, tempfile

# Obtener el valor actual de la UF
def obtener_valor_uf():
    url = "https://www.mindicador.cl/api/uf/"
    respuesta = requests.get(url)
    data = respuesta.json()
    return data['serie'][0]['valor']

# Calcular la tabla de amortización
def tabla_amort_en_uf(valor_propiedad, porc_financ,tasa_anual, plazo_anos, tipo_moneda = 'uf'):

    global detalle_consulta, moneda

    moneda = tipo_moneda.upper()
    
    detalle_consulta = detalles(valor_propiedad, porc_financ, tasa_anual, plazo_anos)

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
def tabla_amortizacion_en_clp(valor_propiedad, porc_financ, tasa_anual, plazo_anos, tipo_moneda='clp'):

    global detalle_consulta, moneda
    
    moneda = tipo_moneda.upper()
    
    detalle_consulta = detalles(valor_propiedad, porc_financ, tasa_anual, plazo_anos)

    valor_uf = obtener_valor_uf()
    df_uf = tabla_amort_en_uf(valor_propiedad, porc_financ, tasa_anual, plazo_anos)
    df_clp = df_uf.copy()
    df_clp["Cuota"] = df_clp["Cuota"] * valor_uf
    df_clp["Interés"] = df_clp["Interés"] * valor_uf
    df_clp["Amortización"] = df_clp["Amortización"] * valor_uf
    df_clp["Saldo"] = df_clp["Saldo"] * valor_uf
    return df_clp

# Detalle de la consulta
def detalles(valor_propiedad, porc_financ, tasa_anual, plazo_anos):
    if moneda.lower() == 'clp':
        valor_uf = obtener_valor_uf()
        valor_propiedad = valor_propiedad * valor_uf
        prestamo = valor_propiedad * (porc_financ / 100)
    else:
        prestamo = valor_propiedad * (porc_financ / 100)
    detalle = []
    detalle.append(valor_propiedad)
    detalle.append(porc_financ)
    detalle.append(tasa_anual)
    detalle.append(plazo_anos)
    detalle.append(prestamo)

    return detalle

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
    # Preparar datos para la tabla
    data = [list(tabla.columns)] + tabla.values.tolist()
    # Crear PDF 
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        pdf = PDF(tmp.name)
        pdf.add_title(f'Detalle de amortización del crédito hipotecario en {moneda}')
        pdf.add_paragraph(f"{detalle_consulta[0]:.0f} {moneda} a un plazo de {detalle_consulta[3]} años, con un financiamiento del {detalle_consulta[1]:.1f}% y una tasa anual del {detalle_consulta[2]:.2f}%")
        pdf.add_table(data)
        pdf.build()
        tmp.seek(0)
        output = io.BytesIO(tmp.read())
    os.unlink(tmp.name)
    output.seek(0)
    return output                  

# Formatear datos a 2 decimales
def formatear_dataframe(df):
    df_formateado = df.copy()
    for col in df_formateado.columns:
        if col != "Mes":
            df_formateado[col] = df_formateado[col].apply(lambda x: f"{x:.2f}")
    return df_formateado  
