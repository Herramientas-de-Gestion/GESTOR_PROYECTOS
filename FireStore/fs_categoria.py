from Controllers.ctr_categoria import Controll_Categoria
from Models.models import Categoria
def categorias_listado():
    controlador = Controll_Categoria()
    return controlador.listar_categorias()

def categoria_registrado( obj_cat:Categoria):
    mensaje_registrar = ""
    if(obj_cat.nombre_categoria== "" ):
        mensaje_registrar = "El nombre no puede estar vacio"
        return mensaje_registrar
    return "categoria creado exitosamente" 