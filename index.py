#IMPORTACIONES NECESARIAS DE CLASES Y METODOS NECESARIOS
from flask import Flask, render_template,request,url_for,redirect,session
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

#IMPORTACION DE MODELS
from Models.models import db,Proyecto, Usuario, Tarea, Estado, Prioridad, Categoria

#IMPORTACION DE SETTINGS
from Settings.settings import get_sqlalchemy_uri

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
#============================================================================================================
# ================================ RUTA PARA LA SECCION REGISTRO  ===========================================
@app.route('/registro_vista', methods=['GET', 'POST'])
def registro_vista():
    return render_template('registro.html')
#============================================================================================================
if __name__ == '__main__':
    app.run(debug=True, port=9000)

