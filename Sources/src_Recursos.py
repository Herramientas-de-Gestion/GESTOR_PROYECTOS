#IMPORTACIONES NECESARIAS
import hashlib
import uuid

class CN_Recursos():
    #ESTA FUNCION ME PERMITE CONVERTIR LA CONTRASEÑA EN UN TEXTO ENCRIPTADO
    def convertir_hash(self,texto):
        sha256 = hashlib.sha256()
        sha256.update(texto.encode('utf-8'))
        return sha256.hexdigest()

    #ESTA OTRA FUNCION ME PERMITE GENERAR UNA CLAVE ALEATORIA DE 6 DIGITOS
    def generar_clave():
        clave = uuid.uuid4().hex[:6]
        return clave
