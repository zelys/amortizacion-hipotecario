# Calculadora de Amortización de Crédito Hipotecario

Una aplicación web simple y efectiva para calcular y visualizar la tabla de amortización de créditos hipotecarios. Permite a los usuarios entender cómo se distribuyen los pagos de su crédito a lo largo del tiempo, separando capital e intereses.

---

### Ver en Vivo

**Puedes probar la aplicación desplegada en Vercel aquí:** [Enlace a la aplicación](https://amortizacion-hipotecario.vercel.app)

---

## Características Principales

- **Doble Moneda:** Calcula la amortización tanto en **Pesos Chilenos (CLP)** como en **Unidades de Fomento (UF)**.
- **Visualización Clara:** Muestra una tabla detallada con el mes, cuota, interés, amortización y saldo restante.
- **Exportación de Datos:** Descarga la tabla de amortización completa en formatos **Excel (.xlsx)**, **CSV (.csv)** y **PDF (.pdf)** para tus registros.
- **Diseño Responsivo:** Interfaz limpia y fácil de usar que funciona en computadores de escritorio y dispositivos móviles.
- **Valor de la UF en Tiempo Real:** Obtiene el valor actualizado de la UF automáticamente para realizar los cálculos.

## Tecnologías Utilizadas

- **Backend:** Python con [Flask](https://flask.palletsprojects.com/)
- **Cálculo de Datos:** [Pandas](https://pandas.pydata.org/) y [NumPy](https://numpy.org/)
- **Generación de Archivos:**
  - Excel: `openpyxl`
  - PDF: `fpdf`
- **Frontend:** HTML (con plantillas Jinja2)
- **Estilos:** Tailwind CSS
- **API para UF:** [Mindicador](https://www.mindicador.cl/api/uf) para obtener
- **Despliegue:** [Vercel](https://vercel.com)

## Instalación y Ejecución Local

Sigue estos pasos para ejecutar el proyecto en tu propia máquina.

1.  **Clona el repositorio:**

    ```bash
    git clone https://github.com/zelys/amortizacion-hipotecario.git
    cd amortizacion-hipotecario
    ```

2.  **Crea y activa un entorno virtual:**

    ```bash
    # En macOS o Linux
    python3 -m venv .venv
    source .venv/bin/activate

    # En Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Instala las dependencias de Python:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Instala y compila Tailwind CSS:**

    ```bash
    # Instala las dependencias de Node.js
    npm install

    # Compila el CSS para producción
    npm run build-css
    ```

5.  **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

6.  **Ejecuta la aplicación Flask:**
    ```bash
    flask --app app run --debug
    ```
    La aplicación estará disponible en `http://127.0.0.1:5000` en tu navegador.

## Uso de la Aplicación

1.  Abre la aplicación en tu navegador.
2.  Selecciona si el valor de la propiedad está en UF o CLP.
3.  Ingresa el valor de la propiedad, el porcentaje a financiar, la tasa de interés anual y el plazo en años.
4.  Haz clic en "Calcular" para ver la tabla de amortización.
5.  Si deseas, puedes usar los botones "Descargar Excel" o "Descargar PDF" para exportar la tabla.

## Contribuciones

Si deseas contribuir al proyecto, ¡serás bienvenido! Aquí hay algunas formas en las que puedes ayudar:

- Reportar errores o sugerir mejoras abriendo un **issue**.
- Enviar **pull requests** con correcciones o nuevas características.

## Licencia

Este proyecto está bajo la licencia [MIT](https://opensource.org/license/mit/). Puedes usar, modificar y distribuir el código libremente, siempre que incluyas la licencia original en tus distribuciones.

## Creditos

Este proyecto fue creado por [Zelys](https://linkedin.com/in/ecelis) y es parte de su portafolio de proyectos. Si tienes alguna pregunta o comentario, no dudes en contactarme.
