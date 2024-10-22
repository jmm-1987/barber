from flask_sqlalchemy import SQLAlchemy

# Instancia de SQLAlchemy
db = SQLAlchemy()


# Modelo de Cita
class Cita(db.Model):
    __tablename__ = 'citas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.String(10), nullable=False)  # Formato de fecha: '2024-10-02'
    hora = db.Column(db.String(5), nullable=False)  # Formato de hora: '14:00'
    usuario = db.Column(db.String(5), nullable=False)
    telefono = db.Column(db.String(5), nullable=False)
    estado = db.Column(db.String(10), default='disponible')  # 'disponible' o 'ocupada'


    def __repr__(self):
        return f'<Cita {self.fecha} {self.hora}>'
