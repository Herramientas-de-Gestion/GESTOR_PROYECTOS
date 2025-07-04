from Models.models import Categoria

class Controll_Categoria():
    def listar_categorias(self):
        categoria= Categoria.query.all()
        return categoria