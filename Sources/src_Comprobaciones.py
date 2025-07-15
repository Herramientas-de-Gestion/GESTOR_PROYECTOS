from Models.models import Estado,Prioridad,Categoria

class Comprobaciones():
    def mostrar_console():
        print("==============ESTADO=================")
        estado = Estado.query.all()
        for est in estado:
            print(est.nombre_estado)
        print("===============PRIORIDAD================")
        prioridad = Prioridad.query.all()
        for prio in prioridad:
            print(prio.nombre_prioridad)
        print("===============CATEGORIA================")
        categoria = Categoria.query.all()
        for cate in categoria:
            print(cate.nombre_categoria)