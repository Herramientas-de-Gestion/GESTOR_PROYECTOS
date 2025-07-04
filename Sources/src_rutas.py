from flask import Flask, render_template,request,url_for,redirect,session
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'correo_usuario' not in session:  # Verificar si el usuario está autenticado
            return render_template('login.html', message="Debes iniciar sesión primero")
        return f(*args, **kwargs)
    return decorated_function 