import pandas as pd
from fpdf import FPDF
import io

def calcular_tabla_amortizacion(valor, porcentaje, tasa, plazo):
    monto = valor * porcentaje / 100
    tasa_mensual = tasa / 12 / 100
    n_pagos = plazo * 12
    cuota = monto * (tasa_mensual * (1 + tasa_mensual) ** n_pagos) / ((1 + tasa_mensual) ** n_pagos - 1)
    saldo = monto
    tabla = []
    for i in range(1, n_pagos + 1):
        interes = saldo * tasa_mensual
        abono = cuota - interes
        saldo -= abono
        tabla.append({
            'Mes': i,
            'Cuota': round(cuota, 2),
            'Interés': round(interes, 2),
            'Abono a capital': round(abono, 2),
            'Saldo': round(max(saldo, 0), 2)
        })
    return pd.DataFrame(tabla)

def exportar_excel(tabla):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        tabla.to_excel(writer, index=False)
    output.seek(0)
    return output

def exportar_pdf(tabla):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    col_width = pdf.w / (len(tabla.columns) + 1)
    row_height = pdf.font_size * 1.5
    for col in tabla.columns:
        pdf.cell(col_width, row_height, str(col), border=1)
    pdf.ln(row_height)
    pdf.set_font('Arial', '', 10)
    for _, row in tabla.iterrows():
        for item in row:
            pdf.cell(col_width, row_height, str(item), border=1)
        pdf.ln(row_height)
    output = io.BytesIO(pdf.output(dest='S').encode('latin1'))
    output.seek(0)
    return output