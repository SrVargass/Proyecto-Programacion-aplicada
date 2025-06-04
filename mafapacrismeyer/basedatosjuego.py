import json

class Basedatosjuego():
    def __init__(self, filename):
        self._filename = filename
        with open(self._filename, "r") as json_file:
            json_str = json_file.read()
            self.dict = json.loads(json_str)

    def crear_entrada(self, clave, valor):
        self.dict[clave] = valor

    def eliminar_entrada(self, clave):
        self.dict.pop(clave)

    def actualizarJson(self):
        with open(self._filename, "w") as json_file:
            json_str = json.dumps(self.dict)
            json_file.write(json_str)

    def existe(self, clave):
        return clave in self.dict.keys()

class BasePersonajes(Basedatosjuego):
    def crear_personaje(self, nombre, stats):
        if not self.existe(nombre):
            self.crear_entrada(nombre, stats)
            self.actualizarJson()
            return True
        return False
    
    def actualizar_stat(self, nombre, stat, valor):
        if self.existe(nombre):
            self.dict[nombre][stat] = valor
            self.actualizarJson()
            return True
        return False

class GestorArmas(Basedatosjuego):
    def modificar_daño(self, arma, nuevo_daño):
        if self.existe(arma):
            self.dict[arma]["daño"] = nuevo_daño
            self.actualizarJson()
            return True
        return False

class GestorPartidas(Basedatosjuego):
    def registrar_partida(self, partida, datos):
        self.crear_entrada(partida, datos)
        self.actualizarJson()

    def obtener_ranking(self):
        return sorted(self.dict.items(), 
                    key=lambda x: x[1].get("enemigos_derrotados", 0), 
                    reverse=True)

class GestorMovimientos(Basedatosjuego):
    def asignar_tecla(self, movimiento, tecla):
        if self.existe(movimiento):
            if "tecla" not in self.dict[movimiento]:
                self.dict[movimiento]["tecla"] = ""
            self.dict[movimiento]["tecla"] = tecla
            self.actualizarJson()
            return True
        return False
