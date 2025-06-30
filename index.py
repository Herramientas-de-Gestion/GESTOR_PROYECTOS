#IMPORTACIONES NECESARIAS DE CLASES Y METODOS NECESARIOS
from flask import Flask, render_template,request,url_for,redirect,session
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

#IMPORTACION DE MODELS
from Models.models import db,Proyecto, Usuario, Tarea, Estado, Prioridad, Categoria

#IMPORTACION DE SETTINGS
from Settings.settings import get_sqlalchemy_uri

#IMPORTACIN DE CONTROLLERS
from Controllers.ctr_usuarios import CD_Usuario

#IMPORTACIN DE CONTROLLERS
from FireStore.fs_usuarios import CN_Usuarios

#IMPORTACION DE SOURCES
from Sources.src_Recursos import CN_Recursos
from Sources.src_Correo import Enviar_correo

#INICIALIZACION DE LA APP FLASK
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_sqlalchemy_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'tu_clave_secreta'
db.init_app(app)
migrate = Migrate(app, db) 
ma = Marshmallow(app)

#GENERACION DE LOS MODELOS DE BASE DE DATOS
with app.app_context():
    db.create_all()

# ================================ RUTA RAIZ DIRIGIENDO A UNA RUTA ESPECIFICA ===============================
@app.route('/')
def home():
    return redirect(url_for('login'))
#============================================================================================================
# ================================ RUTA PARA EL LOGIN PRINCIPAL =============================================
@app.route('/login',methods=['GET', 'POST'] )
def login():
    return render_template('login.html')
#RUTA PARA ENVIAR DATOS 
@app.route('/enviar_datos', methods=['GET', 'POST'])
def enviar_datos():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        contraseña = CN_Recursos().convertir_hash(contraseña)
        usuario = CD_Usuario().consultar_usuario(correo,contraseña)
        if usuario:
            session['id_usuario'] = usuario.id_usuario
            session['nombre_usuario'] = usuario.nombre_usuario
            session['correo_usuario'] = usuario.correo_usuario
            session['apellido_usuario'] = usuario.apellido_usuario
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login', mensaje='Correo o contraseña incorrectos'))
    return redirect(url_for('login'))

#RUTA PARA CERRAR LA SESSION
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login')) 
#============================================================================================================
# ================================ RUTA PARA LA SECCION REGISTRO  ===========================================
@app.route('/registro_vista', methods=['GET', 'POST'])
def registro_vista():
    return render_template('registro.html')
#RUTA PARA REALIZAR EL REGISTRO
@app.route('/registro_usuario', methods=['GET', 'POST'])
def registro_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        conf_contraseña = request.form ['conf_contraseña']

        if CN_Usuarios().confirmar_contraseña(contraseña,conf_contraseña):
            mensaje = CN_Usuarios().confirmar_contraseña(contraseña,conf_contraseña)
            return render_template('registro.html',mensaje=mensaje)
        
        obj_user = Usuario(
            nombre_usuario=nombre,
            apellido_usuario=apellido,
            correo_usuario=correo,
            contraseña_usuario=CN_Recursos().convertir_hash(contraseña)
        )

        mensaje = CN_Usuarios().usuario_registrado(obj_user)
        if mensaje == "usuario creado exitosamente":
            Enviar_correo(correo,CN_Recursos().convertir_hash(contraseña))
            mensaje_bueno = "Felicidades, usuario creado exitosamente"
            db.session.add(obj_user)
            db.session.commit()
            return render_template('registro.html',mensaje=mensaje_bueno)
        
    return render_template('registro.html',mensaje=mensaje)
#============================================================================================================
# ================================ RUTA PARA LA SECCION INDEX  ==============================================
@app.route('/index')
def index():
    return render_template('index.html')
#============================================================================================================
if __name__ == '__main__':
    app.run(debug=True, port=9000)

