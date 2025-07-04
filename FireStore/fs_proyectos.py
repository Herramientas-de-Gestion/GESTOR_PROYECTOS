from Controllers.ctr_proyectos import Controll_Proyecto
from Models.models import Proyecto
from flask import session,render_template


def proyectos_listado():
    controlador = Controll_Proyecto()
    return controlador.listar_proyecto()

def proyecto_registrado( obj_proy:Proyecto):
    mensaje_registrar = ""
    if(obj_proy.nombre_proyecto== "" ):
        mensaje_registrar = "El nombre no puede estar vacio"
        return mensaje_registrar
    if(obj_proy.descripcion_proyecto== "" ):
        mensaje_registrar = "La descripción no puede estar vacia"
        return mensaje_registrar
    if(obj_proy.categoria_id== "" ):
        mensaje_registrar = "La categoria no puede estar vacia"
        return mensaje_registrar
    return "proyecto creado exitosamente"