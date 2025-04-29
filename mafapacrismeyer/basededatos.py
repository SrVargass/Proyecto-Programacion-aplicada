import json

class BaseUsuarios():
    def __init__(self, filename):
        self._filename = filename
        with open(self._filename, "r") as json_file:
            json_str = json_file.read()
            self.dict = json.loads(json_str)

    def crear_usuario(self, nombre, clave):
        self.dict[nombre] = clave

    def eliminar_usuario(self, nombre):
        self.dict.pop(nombre)

    def actualizarJson(self):
        with open(self._filename, "w") as json_file:
            json_str = json.dumps(self.dict)
            json_file.write(json_str)

    def existe(self, nombre):
        if nombre in self.dict.keys():
            return True
        else:
            return False


class Usuario():
    def __init__(self,base,nombre):
        self.base = base
        self.nombre = nombre
        self.sesionIniciada = False

    def iniciar_sesion(self, clave):
        if self.base.dict[self.nombre] == clave:
            self.sesionIniciada = True
        else:
            self.sesionIniciada = False
        return self.sesionIniciada

    def cerrar_sesion(self):
        self.sesionIniciada = False


#baseUsuarios = BaseUsuarios("usuarios.json")
#baseUsuarios.crear_usuario("tralalero","tralala")
#print(baseUsuarios.dict)
#baseUsuarios.actualizarJson()
#user = Usuario(baseUsuarios, "jose")
#print(user.sesionIniciada)
#print(user.iniciar_sesion("joselit0123"))
#print(user.sesionIniciada)
#user.cerrar_sesion()
#print(user.sesionIniciada)
