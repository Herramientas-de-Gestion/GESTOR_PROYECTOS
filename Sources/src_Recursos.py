#IMPORTACIONES NECESARIAS
from flask import render_template, session
from functools import wraps
import hashlib
import uuid

class CN_Recursos():
    #ESTA FUNCION ME PERMITE CONVERTIR LA CONTRASEÑA EN UN TEXTO ENCRIPTADO
    def convertir_hash(self,texto):
        sha256 = hashlib.sha256()
        sha256.update(texto.encode('utf-8'))
        return sha256.hexdigest()

    #ESTA OTRA FUNCION ME PERMITE GENERAR UNA CLAVE ALEATORIA DE 6 DIGITOS
    def generar_clave():
        clave = uuid.uuid4().hex[:6]
        return clave

    #ESTA FUNCION ME PERMITE PROTEGER LAS RUTAS DONDE NO ME HAYA LOGEADO
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'correo_usuario' not in session:  # Verificar si el usuario está autenticado
                return render_template('login.html', message="Debes iniciar sesión primero")
            return f(*args, **kwargs)
        return decorated_function 
