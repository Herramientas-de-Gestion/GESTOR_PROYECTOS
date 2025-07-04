from Controllers.ctr_usuarios import CD_Usuario
from Models.models import Usuario
from Sources.src_Recursos import CN_Recursos

class CN_Usuarios():
    def usuarios_listado(self):
        controlador = CD_Usuario()
        return controlador.listar_usuario()

    def usuario_registrado(self, obj_user: Usuario):
        # Validaciones
        if obj_user.nombre_usuario.strip() == "":
            return "El nombre no puede estar vacío"
        if obj_user.apellido_usuario.strip() == "":
            return "El apellido no puede estar vacío"
        if obj_user.correo_usuario.strip() == "":
            return "El correo no puede estar vacío"
        if obj_user.contraseña_usuario.strip() == "":
            return "La contraseña no puede estar vacía"

        CD_Usuario().agregar_usuario(obj_user)
        return "usuario creado exitosamente"

    #Confirmar la contraseña
    def confirmar_contraseña(self, contraseña, conf_contraseña):
        if contraseña != conf_contraseña:
            return "Las contraseñas no coinciden"
        return None
    
    #Consultar si el usuario existe para iniciar session
    def consultar_usuario(self, correo,password):
        return Usuario.query.filter_by(correo_usuario=correo,contraseña_usuario=password).first()