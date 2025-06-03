import json
from pathlib import Path


class Basedatosjuego():
    def __init__(self, filename):
        self._filename =Path(filename)
        self.cargar_datos()
        

    def cargar_datos(self):
        try:
            with open(self._filename, 'r', encoding='utf-8') as f:
                self.datos= json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.datos= {}
    def guardar_datos(self):
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(self.datos, f, indent=2, ensure_ascii=False)

    def agregar_entrada(self, clave, valor):
        self.datos[clave]= valor
        self.guardar_datos()

    def eliminar_entrada(self, clave):
        if clave in self.datos():
            del self.datos[clave]
            self.guardar_datos()
    
    def existe(self, clave):
        return clave in self.datos
    
class GestorPersonajes(Basedatosjuego):

    def crear_personaje(self, nombre, stats):
        if not self.existe(nombre):
            self.agregar_entrada(nombre,stats)
            return True
        return False
    
    def actualizar_stat(self,nombre,stat,valor):
        if self.existe(nombre):
            self.datos[nombre][stat]=valor
            self.guardar_datos()
            return True
        return False

class GestorArmas(Basedatosjuego):
    def modificar_daño(self,arma,nuevo_daño):
        if self.existe(arma):
            self.datos[arma]["daño"]=nuevo_daño
            self.guardar_datos
            return True
        return False

class GestorPartidas(Basedatosjuego):
    def registrar_partida(self,partida,datos):
        self.agregar_entrada(partida,datos)

    def obtener_ranking(self):
        return sorted(self.datos.items(), key=lambda x: x[1].get("puntuacion",0), reverse=True)
    

class GestorMovimientos(Basedatosjuego):
    def asignar_tecla(self,movimiento, tecla):
        if self.existe(movimiento):
            self.datos[movimiento]["tecla"]= tecla
            self.guardar_datos()

if __name__=="__main__":
    personaje_db=GestorPersonajes("data/personaje.json")
    armas_db= GestorArmas("data/armas.json")

    personaje_db.crear_personaje("magico",{
        "vida": 60,
        "velocidad": 25,
        "experiencia": 800
    })
    armas_db.modificar_daño("pistola",55)