import os
import json
import pygame
import pygame_gui
from tkinter import Tk, filedialog
from pathlib import Path
import shutil

# Configuración
SCREEN_RES = (800, 600)
FONDOS_DIR = os.path.join("juego", "resource","background")
CONFIG_FILE = "fondos.json"

class FondoManager:
    def __init__(self, screen):
        self.screen = screen
        self.manager = pygame_gui.UIManager(SCREEN_RES)
        self.background = pygame.Surface(SCREEN_RES)
        self.background.fill((30, 30, 40))
        
        os.makedirs(FONDOS_DIR, exist_ok=True)
        self.config = self._cargar_config()
        self.cambios_pendientes = {}
        self._setup_ui()
        self.root = Tk()
        self.root.withdraw()
   
    def _cargar_config(self):
        """Carga la configuración inicial"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if not all(key in config for key in ["fondos", "fondo_actual"]):
                        raise ValueError("Estructura inválida")
                    
                    fondos_validos = {}
                    for nombre, ruta in config["fondos"].items():
                        if os.path.exists(ruta):
                            fondos_validos[nombre] = ruta
                    
                    if fondos_validos:
                        fondo_actual = config["fondo_actual"] if config["fondo_actual"] in fondos_validos else next(iter(fondos_validos))
                        return {
                            "fondos": fondos_validos,
                            "fondo_actual": fondo_actual
                        }
        except Exception as e:
            print(f"Error cargando configuración: {e}")
        
        return {"fondos": {}, "fondo_actual": None}

    def _guardar_config(self):
        """Guarda la configuración actual en el archivo JSON"""
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def _setup_ui(self):
        """Configura los elementos de la interfaz de usuario"""
        # Panel principal
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(20, 20, 250, 560),
            manager=self.manager,
            object_id="#main_panel"
        )
        
        # Botones
        self.boton_agregar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (230, 40)),
            text="➕ Agregar Fondo",
            manager=self.manager,
            container=self.panel
        )
        
        self.boton_eliminar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 60), (230, 40)),
            text="🗑️ Eliminar Fondo",
            manager=self.manager,
            container=self.panel
        )
        
        self.boton_actualizar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 110), (230, 40)),
            text="🔄 Aplicar Cambios (0)",
            manager=self.manager,
            container=self.panel
        )
        
        # --> NUEVO BOTÓN VOLVER <--
        self.boton_volver = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 500), (230, 40)),
            text="← Volver",
            manager=self.manager,
            container=self.panel,
            object_id="#back_button"
        )
        
        # Lista desplegable
        opciones = list(self.config["fondos"].keys()) if self.config["fondos"] else ["No hay fondos"]
        self.lista_fondos = pygame_gui.elements.UIDropDownMenu(
            options_list=opciones,
            starting_option=self.config["fondo_actual"] if self.config["fondo_actual"] in opciones else (opciones[0] if opciones else ""),
            relative_rect=pygame.Rect((10, 160), (230, 40)),
            manager=self.manager,
            container=self.panel
        )
        
        # Área de previsualización
        self.preview_rect = pygame.Rect(300, 50, 450, 300)
        
        # Etiquetas
        self.etiqueta_estado = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 210), (230, 30)),
            text=f"Fondo actual: {self.config['fondo_actual'] or 'Ninguno'}",
            manager=self.manager,
            container=self.panel
        )

    def _actualizar_ui(self):
        """Actualiza todos los elementos de la UI"""
        opciones = list(self.config["fondos"].keys()) if self.config["fondos"] else ["No hay fondos"]
        
        # Recrear el dropdown completamente (solución más estable)
        rect = self.lista_fondos.relative_rect
        self.lista_fondos.kill()
        self.lista_fondos = pygame_gui.elements.UIDropDownMenu(
            options_list=opciones,
            starting_option=self.config["fondo_actual"] if self.config["fondo_actual"] in opciones else (opciones[0] if opciones else ""),
            relative_rect=rect,
            manager=self.manager,
            container=self.panel
        )
        
        self.etiqueta_estado.set_text(f"Fondo actual: {self.config['fondo_actual'] or 'Ninguno'}")
        self.boton_actualizar.set_text(f"🔄 Aplicar ({len(self.cambios_pendientes)})")

    def _agregar_fondo(self):
        """Abre el diálogo para seleccionar y agregar un nuevo fondo"""
        filetypes = [("Imágenes", "*.png *.jpg *.jpeg")]
        ruta = filedialog.askopenfilename(title="Seleccionar fondo", filetypes=filetypes)
        
        if ruta:
            try:
                # Verificar que es una imagen válida
                pygame.image.load(ruta)
                
                # Obtener nombre del archivo (sin extensión)
                nombre = Path(ruta).stem
                
                # Generar nombre único
                contador = 1
                nombre_original = nombre
                while nombre in [*self.config["fondos"].keys(), *self.cambios_pendientes.keys()]:
                    nombre = f"{nombre_original}_{contador}"
                    contador += 1
                
                # Agregar a cambios pendientes
                self.cambios_pendientes[nombre] = {
                    'ruta': ruta,
                    'accion': 'agregar'
                }
                self._actualizar_ui()
                
            except Exception as e:
                print(f"Error al procesar imagen: {e}")

    def _eliminar_fondo(self):
        """Marca el fondo seleccionado para eliminación"""
        fondo_seleccionado = self.lista_fondos.selected_option
        if isinstance(fondo_seleccionado, tuple):
            fondo_seleccionado = fondo_seleccionado[0]
        
        if fondo_seleccionado and fondo_seleccionado in self.config["fondos"]:
            self.cambios_pendientes[fondo_seleccionado] = {
                'accion': 'eliminar'
            }
            self._actualizar_ui()
            print(f"Fondo marcado para eliminar: {fondo_seleccionado}")

    def _aplicar_cambios(self):
        """Aplica todos los cambios pendientes (agregar/eliminar)"""
        if not self.cambios_pendientes:
            print("No hay cambios pendientes para aplicar")
            return
        
        for nombre, cambio in list(self.cambios_pendientes.items()):
            if cambio['accion'] == 'agregar':
                # Copiar imagen al directorio
                extension = Path(cambio['ruta']).suffix
                nueva_ruta = os.path.join(FONDOS_DIR, f"{nombre}{extension}")
                shutil.copy2(cambio['ruta'], nueva_ruta)
                
                # Agregar al JSON
                self.config["fondos"][nombre] = nueva_ruta
                
            elif cambio['accion'] == 'eliminar' and nombre in self.config["fondos"]:
                # Eliminar archivo físico
                ruta = self.config["fondos"][nombre]
                if os.path.exists(ruta):
                    try:
                        os.remove(ruta)
                        print(f"Archivo eliminado: {ruta}")
                    except Exception as e:
                        print(f"Error eliminando archivo: {e}")
                
                # Eliminar del JSON
                del self.config["fondos"][nombre]
                
                # Actualizar fondo actual si era el que se eliminó
                if self.config["fondo_actual"] == nombre:
                    self.config["fondo_actual"] = next(iter(self.config["fondos"]), None)
        
        self.cambios_pendientes.clear()
        self._guardar_config()
        self._actualizar_ui()
        print("Todos los cambios han sido aplicados")

    def mostrar(self):
        """Bucle principal de la interfaz"""
        fondo_anterior = None
        imagen_cargada = None

        clock = pygame.time.Clock()
        running = True
        
        while running:
            time_delta = clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.boton_agregar:
                        self._agregar_fondo()
                    elif event.ui_element == self.boton_eliminar:
                        self._eliminar_fondo()
                    elif event.ui_element == self.boton_actualizar:
                        self._aplicar_cambios()
                    elif event.ui_element == self.boton_volver:  # Manejo del botón volver
                        return self.config["fondo_actual"]  # Retorna el fondo actual
                
                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == self.lista_fondos:
                        nuevo_fondo = event.text
                        if isinstance(nuevo_fondo, tuple):
                            nuevo_fondo = nuevo_fondo[0]
                        self.config["fondo_actual"] = nuevo_fondo
                        self.etiqueta_estado.set_text(f"Fondo actual: {nuevo_fondo}")
                
                self.manager.process_events(event)
            
            # Dibujado
            self.screen.blit(self.background, (0, 0))
            
            # Previsualización
            fondo_actual = self.config["fondo_actual"]
            if fondo_actual != fondo_anterior:
                fondo_anterior = fondo_actual
                imagen_cargada = None
                if fondo_actual and fondo_actual in self.config["fondos"]:
                    try: 
                        img = pygame.image.load(self.config["fondos"][fondo_actual])
                        imagen_cargada = pygame.transform.scale(img,(self.preview_rect.width,self.preview_rect.height))
                    except Exception as e:
                        print(f"Error cargando imagen: {e}")
                        imagen_cargada = None
            if imagen_cargada:
                self.screen.blit(imagen_cargada, self.preview_rect)
            else:
                pygame.draw.rect(self.screen, (255, 0, 0), self.preview_rect, 2)
            
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.update()
        
        return self.config["fondo_actual"]

def fondo_juego(screen):
    manager = FondoManager(screen)
    return manager.mostrar()