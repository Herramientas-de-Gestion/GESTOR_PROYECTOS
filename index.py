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
from Controllers.ctr_categoria import Controll_Categoria
from Controllers.ctr_proyectos import Controll_Proyecto

#IMPORTACIN DE CONTROLLERS
from FireStore.fs_usuarios import CN_Usuarios
from FireStore.fs_categoria import categorias_listado,categoria_registrado
from FireStore.fs_proyectos import proyectos_listado,proyecto_registrado

#IMPORTACION DE SOURCES
from Sources.src_Recursos import CN_Recursos
from Sources.src_Correo import Enviar_correo
from Sources.src_rutas import login_required

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
        usuario = CN_Usuarios().consultar_usuario(correo,contraseña)
        if usuario:
            print(usuario.id_usuario)
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
    mensaje = ""
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        conf_contraseña = request.form['conf_contraseña']

        # Verificar contraseña
        mensaje_contraseña = CN_Usuarios().confirmar_contraseña(contraseña, conf_contraseña)
        if mensaje_contraseña:
            return render_template('registro.html', mensaje=mensaje_contraseña)

        obj_user = Usuario(
            nombre_usuario=nombre,
            apellido_usuario=apellido,
            correo_usuario=correo,
            contraseña_usuario=contraseña
        )
        mensaje = CN_Usuarios().usuario_registrado(obj_user)

        if mensaje == "usuario creado exitosamente":
            Enviar_correo(correo, contraseña)
            mensaje_bueno = "Felicidades, usuario creado exitosamente"
            return render_template('registro.html', mensaje=mensaje_bueno)

    return render_template('registro.html', mensaje=mensaje)


# ===================================== CREAR CATEGORIA ====================================
@login_required
@app.route('/nueva_categoria', methods=['POST'])
def nueva_categoria():
    print('Creando categoria')
    if request.method == 'POST':
        nombreCat = request.form['nombreCat']
        obj_cat = Categoria(
            nombre_categoria=nombreCat,
        )
        print(obj_cat)
        mensaje = categoria_registrado(obj_cat)
        if mensaje == "categoria creado exitosamente":
            mensaje_bueno = "Felicidades, categoria creado exitosamente"
            db.session.add(obj_cat)
            db.session.commit()
            return render_template('index.html',mensaje=mensaje_bueno)
    return render_template('index.html')


# ===================================== CREAR PROYECTO ====================================

@login_required
@app.route('/nuevo_proyecto', methods=['POST'])
def nuevo_proyecto():
    print('Entraste')
    if request.method == 'POST':
        titulo = request.form['tarea']
        descripcion = request.form['descripcion']
        categoria = request.form['mi_select']
        usuario = session.get('id_usuario')
        obj_proy = Proyecto(
            nombre_proyecto=titulo,
            descripcion_proyecto=descripcion,
            categoria_id=categoria,
            usuario_id_p=usuario,
        )
        print(obj_proy)
        mensaje = proyecto_registrado(obj_proy)
        if mensaje == "proyecto creado exitosamente":
            mensaje_bueno = "Felicidades, usuario creado exitosamente"
            db.session.add(obj_proy)
            db.session.commit()
            return render_template('index.html',mensaje=mensaje_bueno)
    return render_template('index.html')


# ===================================== LISTAR PROYECTOS ====================================

@login_required
@app.route('/proyectos', methods=['GET', 'POST'])
def proyectos():
    correo = session.get('correo_usuario', 'Usuario no identificado')
    nombre = session.get('nombre_usuario', 'Usuario no identificado')
    apellido = session.get('apellido_usuario', 'Usuario no identificado')
    categoria = Categoria.query.all()
    usuario_id = session.get('id_usuario')
    proyectos = Proyecto.query.filter_by(usuario_id_p=usuario_id).all()
    print('Mostrando los datos del proyecto')
    for proy in proyectos:
        nombre = proy.nombre_proyecto
        descripcion = proy.descripcion_proyecto
        categoria = proy.categoria_id
        print(f'nombre: {nombre} descripcion: {descripcion} categoria: {categoria}')
    return render_template('proyectos.html', proyectos=proyectos,categoria=categoria,nombre=nombre,apellido=apellido)

# ===================================== MOSTRAR PROYECTO ====================================
@login_required
@app.route('/proyecto/<int:proyecto_id>')
def ver_proyecto(proyecto_id):
    proyecto = Proyecto.query.get_or_404(proyecto_id)
    tareas = Tarea.query.filter_by(proyecto_id=proyecto_id).all()
    return render_template('proyecto_detalle.html', proyecto=proyecto, tareas=tareas)


#============================================================================================================

# ================================ RUTA PARA LA SECCION INDEX  ==============================================
@app.route('/index')
def index():
    cd= CN_Usuarios()
    listar_usuarios= cd.usuarios_listado()
    correo = session.get('correo_usuario', 'Usuario no identificado')
    nombre = session.get('nombre_usuario', 'Usuario no identificado')
    apellido = session.get('apellido_usuario', 'Usuario no identificado')
    id_usuario = session.get('id_usuario') 
    print("==============ESTADO=================")
    estado = Estado.query.all()
    for est in estado:
        print(est.nombre_estado)
    print("===============PRIORIDAD================")
    prioridad = Prioridad.query.all()
    for prio in prioridad:
        print(prio.nombre_prioridad)
    print("===============CATEGORIA================")
    categoria = Categoria.query.all()
    for cate in categoria:
        print(cate.nombre_categoria)
    return render_template('index.html',listar_usuarios=listar_usuarios,correo=correo, nombre=nombre,
                            apellido=apellido, estado=estado, prioridad=prioridad, categoria=categoria)
#============================================================================================================
@app.route('/prueba')
def prueba():
    return render_template('layaout.html')
if __name__ == '__main__':
    app.run(debug=True, port=9000)

