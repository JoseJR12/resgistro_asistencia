from flask import Flask, render_template, request, redirect, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'asistencia2025'

CSV_PATH = os.path.join(os.path.dirname(__file__), 'data', 'estudiantes_limpio.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dni = request.form['dni'].strip()

        try:
            # Usa ; como separador y limpia columnas
            df = pd.read_csv(CSV_PATH, sep=';', dtype={'dni': str})
            df.columns = df.columns.str.strip().str.lower()
        except FileNotFoundError:
            flash("Archivo CSV no encontrado", "error")
            return redirect('/')

        if 'dni' not in df.columns:
            flash("La columna 'dni' no existe en el CSV", "error")
            return redirect('/')

        estudiante = df[df['dni'].str.strip() == dni]

        if estudiante.empty:
            flash("DNI no encontrado", "error")
        else:
            index = estudiante.index[0]
            nombre_completo = estudiante.iloc[0]['nombres y apellidos']
            laboratorio = estudiante.iloc[0]['laboratorio']

            df.at[index, 'asistio'] = 'Sí asistió al Examen General 2025-2'
            df.to_csv(CSV_PATH, index=False, sep=';')  # Guarda con el mismo separador

            flash(f"{nombre_completo} se registró correctamente. Le corresponde el {laboratorio}.", "success")

        return redirect('/')

    return render_template('index.html')  # Asegúrate de que este archivo esté en la carpeta 'templates'

if __name__ == '__main__':
    app.run(debug=True)