from Models.models import Usuario

class CD_Usuario():
    def listar_usuario(self):
        usuarios= Usuario.query.all()
        return usuarios
    
    def consultar_usuario(self,correo,contraseña):
        usuario_encontrado = Usuario.query.filter_by(correo_usuario=correo, contraseña_usuario=contraseña).first()
        return usuario_encontrado
    
    def escribir_usuario(self,nombre,correo):
        verificar = print(f"Tu nombre de usuario: {nombre} ; tu correo: {correo}")
        return verificar