from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
db = SQLAlchemy()

class Estado(db.Model):
    __tablename__ = 'estado'
    id_estado = db.Column(db.Integer, primary_key=True)
    nombre_estado = db.Column(db.String(100), nullable=False)

class Prioridad(db.Model):
    __tablename__ = 'prioridad'
    id_prioridad = db.Column(db.Integer, primary_key=True)
    nombre_prioridad = db.Column(db.String(100), nullable=False)

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre_categoria = db.Column(db.String(100), nullable=False)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nombre_usuario = db.Column(db.String(100), nullable=False)
    apellido_usuario = db.Column(db.String(100), nullable=False)
    correo_usuario = db.Column(db.String(150), nullable=False)
    contraseña_usuario = db.Column(db.String(130), nullable=False)

class Proyecto(db.Model):
    __tablename__ = 'proyecto'
    id_proyecto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_proyecto = db.Column(db.String(150), nullable=False)
    descripcion_proyecto = db.Column(db.String(150), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=False)
    fcreacion_proyecto = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id_p = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    # Relaciones (opcional, pero recomendable)
    usuario = db.relationship('Usuario', backref='usuario')
    categoria = db.relationship('Categoria', backref='tareas')

class Tarea(db.Model):
    __tablename__ = 'tarea'
    id_tarea = db.Column(db.Integer, primary_key=True,autoincrement=True)
    titulo_tarea = db.Column(db.String(150), nullable=False)
    descripcion_tarea = db.Column(db.String(500), nullable=True)
    fcreacion_tarea = db.Column(db.DateTime, default=datetime.utcnow)
    fvencimiento_tarea = db.Column(db.DateTime, nullable=True)

    prioridad_id = db.Column(db.Integer, db.ForeignKey('prioridad.id_prioridad'), nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id_estado'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyecto.id_proyecto'), nullable=True)
    
    # Relaciones (opcional, pero recomendable)
    prioridad = db.relationship('Prioridad', backref='tareas')
    estado = db.relationship('Estado', backref='tareas')
    usuario = db.relationship('Usuario', backref='tareas')
    proyecto = db.relationship('Proyecto', backref='tareas')
