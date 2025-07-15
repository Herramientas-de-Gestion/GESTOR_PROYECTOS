from Models.models import Proyecto,Tarea

class Cantidades():
    def mostrar_proyectos(self,id_usuario):
        print("===============PROYECTOS ================")
        cantidad_proyectos=0
        proyectos = Proyecto.query.filter_by(usuario_id_p=id_usuario).all()
        for proy in proyectos:
            cantidad_proyectos+=1
            print(proy.nombre_proyecto)
        print(cantidad_proyectos)
        return cantidad_proyectos

    def mostrar_tareas(self,id_usuario):
        print("=============== TAREAS ================")
        cantidad_tareas=0
        tareas = Tarea.query.filter_by(usuario_id=id_usuario).all()
        for tar in tareas:
            cantidad_tareas+=1
            print(tar.titulo_tarea)
        print(cantidad_tareas)
        return cantidad_tareas