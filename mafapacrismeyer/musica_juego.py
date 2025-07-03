import os
import json
import pygame
import pygame_gui
from tkinter import Tk, filedialog
from pathlib import Path
import shutil

# Configuración
SCREEN_RES = (800, 600)
MUSICA_DIR = os.path.join("juego", "resource", "music")
CONFIG_FILE = "musica.json"

class MusicaManager:
    def __init__(self, screen):
        self.screen = screen
        self.manager = pygame_gui.UIManager(SCREEN_RES)
        self.background = pygame.Surface(SCREEN_RES)
        self.background.fill((20, 20, 30))
        
        os.makedirs(MUSICA_DIR, exist_ok=True)
        self.config = self._cargar_config()
        self.cambios_pendientes = {}
        self._setup_ui()
        self.root = Tk()
        self.root.withdraw()
        
        pygame.mixer.init()

    def _cargar_config(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if not all(k in config for k in ["audios", "audio_actual"]):
                        raise ValueError("Estructura inválida")

                    audios_validos = {}
                    for nombre, ruta in config["audios"].items():
                        if os.path.exists(ruta):
                            audios_validos[nombre] = ruta
                    
                    if audios_validos:
                        audio_actual = config["audio_actual"] if config["audio_actual"] in audios_validos else next(iter(audios_validos))
                        return {"audios": audios_validos, "audio_actual": audio_actual}
        except Exception as e:
            print(f"Error cargando configuración: {e}")
        
        return {"audios": {}, "audio_actual": None}

    def _guardar_config(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def _setup_ui(self):
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(20, 20, 250, 560),
            manager=self.manager,
            object_id="#main_panel"
        )
        
        self.boton_agregar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (230, 40)),
            text="➕ Agregar Música",
            manager=self.manager,
            container=self.panel
        )

        self.boton_eliminar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 60), (230, 40)),
            text="🗑️ Eliminar Música",
            manager=self.manager,
            container=self.panel
        )

        self.boton_actualizar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 110), (230, 40)),
            text="🔄 Aplicar Cambios (0)",
            manager=self.manager,
            container=self.panel
        )

        self.boton_volver = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 500), (230, 40)),
            text="← Volver",
            manager=self.manager,
            container=self.panel
        )

        opciones = list(self.config["audios"].keys()) if self.config["audios"] else ["No hay música"]
        self.lista_audios = pygame_gui.elements.UIDropDownMenu(
            options_list=opciones,
            starting_option=self.config["audio_actual"] if self.config["audio_actual"] in opciones else (opciones[0] if opciones else ""),
            relative_rect=pygame.Rect((10, 160), (230, 40)),
            manager=self.manager,
            container=self.panel
        )

        self.etiqueta_estado = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 210), (230, 30)),
            text=f"Música actual: {self.config['audio_actual'] or 'Ninguna'}",
            manager=self.manager,
            container=self.panel
        )

    def _actualizar_ui(self):
        opciones = list(self.config["audios"].keys()) if self.config["audios"] else ["No hay música"]
        rect = self.lista_audios.relative_rect
        self.lista_audios.kill()
        self.lista_audios = pygame_gui.elements.UIDropDownMenu(
            options_list=opciones,
            starting_option=self.config["audio_actual"] if self.config["audio_actual"] in opciones else (opciones[0] if opciones else ""),
            relative_rect=rect,
            manager=self.manager,
            container=self.panel
        )

        self.etiqueta_estado.set_text(f"Música actual: {self.config['audio_actual'] or 'Ninguna'}")
        self.boton_actualizar.set_text(f"🔄 Aplicar ({len(self.cambios_pendientes)})")

    def _agregar_musica(self):
        filetypes = [("Audios", "*.mp3 *.ogg *.wav")]
        ruta = filedialog.askopenfilename(title="Seleccionar música", filetypes=filetypes)

        if ruta:
            try:
                nombre = Path(ruta).stem
                contador = 1
                nombre_original = nombre
                while nombre in [*self.config["audios"].keys(), *self.cambios_pendientes.keys()]:
                    nombre = f"{nombre_original}_{contador}"
                    contador += 1

                self.cambios_pendientes[nombre] = {
                    'ruta': ruta,
                    'accion': 'agregar'
                }
                self._actualizar_ui()

            except Exception as e:
                print(f"Error al agregar música: {e}")

    def _eliminar_musica(self):
        seleccion = self.lista_audios.selected_option
        if isinstance(seleccion, tuple):
            seleccion = seleccion[0]
        
        if seleccion and seleccion in self.config["audios"]:
            self.cambios_pendientes[seleccion] = {'accion': 'eliminar'}
            self._actualizar_ui()

    def _aplicar_cambios(self):
        if not self.cambios_pendientes:
            return

        for nombre, cambio in list(self.cambios_pendientes.items()):
            if cambio['accion'] == 'agregar':
                extension = Path(cambio['ruta']).suffix
                nueva_ruta = os.path.join(MUSICA_DIR, f"{nombre}{extension}")
                shutil.copy2(cambio['ruta'], nueva_ruta)
                self.config["audios"][nombre] = nueva_ruta

            elif cambio['accion'] == 'eliminar' and nombre in self.config["audios"]:
                ruta = self.config["audios"][nombre]
                if os.path.exists(ruta):
                    os.remove(ruta)
                del self.config["audios"][nombre]
                if self.config["audio_actual"] == nombre:
                    self.config["audio_actual"] = next(iter(self.config["audios"]), None)

        self.cambios_pendientes.clear()
        self._guardar_config()
        self._actualizar_ui()

    def mostrar(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            time_delta = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.boton_agregar:
                        self._agregar_musica()
                    elif event.ui_element == self.boton_eliminar:
                        self._eliminar_musica()
                    elif event.ui_element == self.boton_actualizar:
                        self._aplicar_cambios()
                    elif event.ui_element == self.boton_volver:
                        return self.config["audio_actual"]

                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == self.lista_audios:
                        nuevo_audio = event.text
                        if isinstance(nuevo_audio, tuple):
                            nuevo_audio = nuevo_audio[0]
                        self.config["audio_actual"] = nuevo_audio
                        self.etiqueta_estado.set_text(f"Música actual: {nuevo_audio}")

                self.manager.process_events(event)

            self.screen.blit(self.background, (0, 0))
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.update()

        return self.config["audio_actual"]

def musica_juego(screen):
    manager = MusicaManager(screen)
    return manager.mostrar()
