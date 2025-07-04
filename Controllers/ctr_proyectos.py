from Models.models import Proyecto

class Controll_Proyecto():
    def listar_proyecto(self):
        proyecto= Proyecto.query.all()
        return proyecto
    
    def consultar_proyecto(self,titulo,categoria):
        proyecto_encontrado = Proyecto.query.filter_by(nombre_proyecto=titulo, categoria_id=categoria).first()
        return proyecto_encontrado
    
    def escribir_proyecto(self,nombre):
        verificar = print(f"Proyecto: {nombre}")
        return verificar
    def listar_proyectos_usuario(self, id_usuario):
        proyectos = Proyecto.query.filter_by(usuario_id_p=id_usuario).all()
        return proyectos