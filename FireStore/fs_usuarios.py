from Controllers.ctr_usuarios import CD_Usuario
from Models.models import Usuario
from flask import session,render_template

class CN_Usuarios():
    def usuarios_listado():
        controlador = CD_Usuario()
        return controlador.listar_usuario()

    def usuario_registrado(self, obj_user:Usuario):
        mensaje_registrar = ""
        if(obj_user.nombre_usuario== "" ):
            mensaje_registrar = "El nombre no puede estar vacio"
            return mensaje_registrar
        if(obj_user.apellido_usuario== "" ):
            mensaje_registrar = "El apellido no puede estar vacio"
            return mensaje_registrar
        if(obj_user.correo_usuario== "" ):
            mensaje_registrar = "El correo no puede estar vacio"
            return mensaje_registrar
        return "usuario creado exitosamente"

    def confirmar_contraseña(self,contraseña,conf_contraseña):
        if contraseña != conf_contraseña :
            mensaje_contraseña = "La contraseña debe ser la misma 2 3"
            return mensaje_contraseña