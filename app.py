from flask import Flask, jsonify, request, render_template
from models import db, Cita  # Usa la instancia de db de models.py
from flask_jwt_extended import JWTManager
from datetime import datetime

app = Flask(__name__, static_folder='static')

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///peluqueria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Cambia esto a una clave segura

# Inicializa la base de datos y el JWT con la app
db.init_app(app)
jwt = JWTManager(app)


@app.route('/')
def home():
    return render_template('selector.html')

@app.route('/modelo1')
def modelo1():
    return render_template('index1.html')

@app.route('/modelo2')
def modelo2():
    return render_template('index2.html')

@app.route('/modelo3')
def modelo3():
    return render_template('index3.html')

@app.route('/modelo4')
def modelo4():
    return render_template('index4.html')


@app.route('/reservas1')
def mostrar_reservas1():
    return render_template('reservas1.html')

@app.route('/reservas2')
def mostrar_reservas2():
    return render_template('reservas2.html')

@app.route('/reservas3')
def mostrar_reservas3():
    return render_template('reservas3.html')

@app.route('/galeria1')
def mostrar_galeria1():
    return render_template('galeria1.html')

@app.route('/galeria2')
def mostrar_galeria2():
    return render_template('galeria2.html')

@app.route('/galeria3')
def mostrar_galeria3():
    return render_template('galeria3.html')

@app.route('/panel1')
def mostrar_panel1():
    return render_template('panel1.html')

@app.route('/panel2')
def mostrar_panel2():
    return render_template('panel2.html')

@app.route('/panel3')
def mostrar_panel3():
    return render_template('panel3.html')

@app.route('/carta1')
def carta1():
    return render_template('carta1.html')

@app.route('/carta2')
def carta2():
    return render_template('carta2.html')

@app.route('/carta3')
def carta3():
    return render_template('carta3.html')



@app.route('/add_cita', methods=['POST'])
def add_cita():
    data = request.get_json()
    usuario = data.get('usuario')
    telefono = data.get('telefono')
    fecha = data.get('fecha')
    hora = data.get('hora')

    nueva_cita = Cita(fecha=fecha, hora=hora, usuario=usuario, telefono=telefono, estado='ocupada')
    db.session.add(nueva_cita)
    db.session.commit()

    return jsonify({'msg': 'Cita agregada correctamente'}), 201

"""@app.route('/delete_cita', methods=['POST'])
def delete_cita():
    data = request.get_json()
    fecha = data.get('fecha')
    hora = data.get('hora')

    # Buscar la cita por fecha y hora
    cita = Cita.query.filter_by(fecha=fecha, hora=hora).first()

    if not cita:
        return jsonify({'error': 'Cita no encontrada'}), 404

    # Eliminar la cita
    db.session.delete(cita)
    db.session.commit()

    return jsonify({'msg': 'Cita eliminada correctamente'}), 200"""

@app.route('/delete_cita', methods=['POST'])
def delete_cita():
    data = request.get_json()
    cita_id = data.get('id')  # Obtenemos el ID de la cita

    # Buscar la cita por ID
    cita = Cita.query.filter_by(id=cita_id).first()

    if not cita:
        return jsonify({'error': 'Cita no encontrada'}), 404

    # Eliminar la cita
    db.session.delete(cita)
    db.session.commit()

    return jsonify({'msg': 'Cita eliminada correctamente'}), 200

# Ruta para obtener horas disponibles (sin autenticación, pero puedes protegerla si lo necesitas)
@app.route('/available_hours', methods=['GET'])
@app.route('/available_hours', methods=['GET'])
def available_hours():
    fecha = request.args.get('date')


    # Convertir la fecha a un objeto datetime
    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')  # Suponiendo que la fecha tiene el formato 'YYYY-MM-DD'
    except ValueError:
        return jsonify({'error': 'Formato de fecha no válido'}), 400

    # Verificar si es domingo (6 es domingo en weekday())
    if fecha_obj.weekday() == 6:
        return jsonify({'available_hours': [], 'message': 'CERRADO'})

    # Consultar las citas ocupadas
    citas_ocupadas = Cita.query.filter_by(fecha=fecha, estado='ocupada').all()

    horas_ocupadas = [cita.hora for cita in citas_ocupadas]

    # Definir las horas de trabajo
    horas_trabajo = ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
                     '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30']

    # Filtrar las horas ocupadas
    horas_disponibles = [hora for hora in horas_trabajo if hora not in horas_ocupadas]

    # Devolver las horas disponibles
    return jsonify({'available_hours': horas_disponibles, 'message': 'Horas disponibles' if horas_disponibles else 'No hay horas disponibles'})

@app.route('/horarios_dia', methods=['GET'])
def horarios_dia():
    # Obtener la fecha de la solicitud
    fecha = request.args.get('date')

    # Convertir la fecha a un objeto datetime
    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')  # Formato 'YYYY-MM-DD'
    except ValueError:
        return jsonify({'error': 'Formato de fecha no válido'}), 400

    # Verificar si es domingo (6 es domingo en weekday())
    if fecha_obj.weekday() == 6:
        return jsonify({'horarios': [], 'message': 'CERRADO'})

    # Definir las horas de trabajo
    horas_trabajo = ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
                     '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30']

    # Consultar las citas ocupadas
    citas_ocupadas = Cita.query.filter_by(fecha=fecha, estado='ocupada').all()

    # Crear un diccionario con las horas ocupadas y el nombre del usuario
    horas_reservadas = {cita.hora: cita.usuario for cita in citas_ocupadas}

    # Crear la lista de horarios con las horas y nombres de quienes han reservado
    horarios = [{'hora': hora, 'nombre': horas_reservadas.get(hora, '')} for hora in horas_trabajo]

    # Devolver la lista de horarios
    return jsonify({'horarios': horarios})


@app.route('/unavailable_hours', methods=['GET'])
def unavailable_hours():
    # Obtener la fecha de la solicitud
    fecha = request.args.get('date')

    # Filtrar las citas ocupadas en esa fecha
    citas_ocupadas = Cita.query.filter_by(fecha=fecha, estado='ocupada').order_by(Cita.hora).all()

    # Estructurar la información de las citas en un formato más legible
    citas_info = [
        {
            'id': cita.id,
            'hora': cita.hora,
            'usuario': cita.usuario,
            'telefono': cita.telefono,
            'fecha': cita.fecha
        }
        for cita in citas_ocupadas
    ]

    # Imprimir para depuración


    # Retornar las citas ocupadas en formato JSON
    return jsonify({'unavailable_hours': citas_info})

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
