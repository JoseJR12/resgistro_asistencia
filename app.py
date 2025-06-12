import os
from flask import Flask, render_template, request, redirect, flash, url_for
import pandas as pd

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'asistencia2025')

# Ruta al CSV de datos
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
CSV_PATH = os.path.join(DATA_DIR, 'estudiantes_limpio.csv')

# Asegura que exista la carpeta de datos
os.makedirs(DATA_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dni = request.form.get('dni', '').strip()

        if not dni:
            flash("Por favor, ingresa un DNI.", 'error')
            return redirect(url_for('index'))

        try:
            # Lee el CSV
            df = pd.read_csv(CSV_PATH, sep=';', dtype={'dni': str})
            df.columns = df.columns.str.strip().str.lower()
        except FileNotFoundError:
            flash("Archivo de datos no encontrado.", 'error')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error al leer datos: {e}", 'error')
            return redirect(url_for('index'))

        # Verifica columna 'dni'
        if 'dni' not in df.columns:
            flash("La columna 'dni' no existe en el archivo de datos.", 'error')
            return redirect(url_for('index'))

        # Encuentra el estudiante
        estudiante = df[df['dni'].str.strip() == dni]
        if estudiante.empty:
            flash("DNI no encontrado.", 'error')
            return redirect(url_for('index'))

        # Información del estudiante
        idx = estudiante.index[0]
        nombre = estudiante.at[idx, 'nombres y apellidos']
        laboratorio = estudiante.at[idx, 'laboratorio']

        # Asegura columna 'asistio'
        if 'asistio' not in df.columns:
            df['asistio'] = ''

        # Marca asistencia y guarda
        df.at[idx, 'asistio'] = 'Sí asistió al Examen General 2025-2'
        try:
            df.to_csv(CSV_PATH, index=False, sep=';')
        except Exception as e:
            flash(f"Error al guardar datos: {e}", 'error')
            return redirect(url_for('index'))

        flash(f"{nombre} registrado exitosamente. Laboratorio: {laboratorio}.", 'success')
        return redirect(url_for('index'))

    # GET
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
