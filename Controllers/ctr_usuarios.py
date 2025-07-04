from Models.models import Usuario, db
from Sources.src_Recursos import CN_Recursos
class CD_Usuario():
    def listar_usuario(self):
        usuarios= Usuario.query.all()
        return usuarios
    
    def agregar_usuario(self, objt_user: Usuario):
        usuario_agregado = Usuario(
            nombre_usuario=objt_user.nombre_usuario,
            apellido_usuario=objt_user.apellido_usuario,
            correo_usuario=objt_user.correo_usuario,
            contraseña_usuario=CN_Recursos().convertir_hash(objt_user.contraseña_usuario)
        )
        db.session.add(usuario_agregado)
        db.session.commit()
        return usuario_agregado

