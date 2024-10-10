import json
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar flash

# Ruta del archivo JSON
DATA_FILE = 'data.json'

# Función para cargar el horario desde el archivo JSON
def load_schedule():
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

# Función para guardar el horario en el archivo JSON
def save_schedule(schedule):
    with open(DATA_FILE, 'w') as file:
        json.dump(schedule, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_day = None
    lunch_info = None
    schedule = load_schedule()

    if request.method == 'POST':
        selected_date = request.form.get('date')
        if selected_date:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            selected_day = date_obj.strftime('%A')

            # Validar si es sábado o domingo
            if selected_day in ['Saturday', 'Sunday']:
                flash('No hay almuerzo disponible para este día. Por favor selecciona un día de lunes a viernes.', 'warning')
                selected_day = None
            else:
                days_map = {
                    'Monday': 'Lunes',
                    'Tuesday': 'Martes',
                    'Wednesday': 'Miercoles',
                    'Thursday': 'Jueves',
                    'Friday': 'Viernes'
                }
                selected_day = days_map.get(selected_day)

                if selected_day in schedule:
                    lunch_info = schedule[selected_day]
                else:
                    flash('No hay almuerzo programado para este día.', 'warning')
                    selected_day = None

    return render_template('index.html', lunch_info=lunch_info, selected_day=selected_day, schedule=schedule)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        day = request.form.get('day')
        time = request.form.get('time')
        menu = request.form.get('menu')
        image = request.form.get('image')

        schedule = load_schedule()
        # Asegúrate de que 'day' esté en español
        if day not in schedule:
            flash(f'El día {day} no está disponible.', 'danger')
            return redirect(url_for('update'))
        
        schedule[day] = {'time': time, 'menu': menu, 'image': image}
        save_schedule(schedule)

        flash(f'Horario actualizado para {day}.', 'success')
        return redirect(url_for('index'))

    schedule = load_schedule()
    return render_template('update.html', schedule=schedule)

if __name__ == '__main__':
    app.run(debug=True)