# gestor_datos.py (código modificado)
import pygame
import pygame_gui
import json
import os
import sys
from constantes import *

ARCHIVOS_JSON = {
    'Usuarios': 'usuarios.json',
    'Recursos': 'recursos.json',
    'Personaje': 'personaje.json',
    'Partida': 'partida.json',
    'Movimiento': 'movimiento.json'
}

CAMPOS_POR_ARCHIVO = {
    'Usuarios': {
        'tipo': 'dict_simple',
        'campos': {'Contraseña': 'str'}
    },
    'Recursos': {
        'tipo': 'objeto',
        'campos': {'tipo': 'str', 'daño': 'int'}
    },
    'Personaje': {
        'tipo': 'objeto',
        'campos': {'vida': 'int', 'velocidad': 'int', 'experiencia': 'int'}
    },
    'Partida': {
        'tipo': 'objeto',
        'campos': {
            'nivel': 'int',
            'dificultad': 'str',
            'duracion': 'int',
            'enemigos_derrotados': 'int',
            'resultado': 'str'
        }
    },
    'Movimiento': {
        'tipo': 'objeto',
        'campos': {'descripcion': 'str', 'tecla': 'str'}
    }
}
def convertir_tipo(valor, tipo):
    if tipo == 'int':
        try:
            return int(valor)
        except ValueError:
            return valor
    elif tipo == 'float':
        try:
            return float(valor)
        except ValueError:
            return valor
    elif tipo == 'bool':
        return valor.lower() in ('true', '1', 'sí', 'si')
    return valor  # str por defecto


def asegurarse_archivo(path):
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({}, f)
    else:
        if os.path.getsize(path) == 0:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({}, f)

def cargar_contenido(path):
    with open(path, 'r', encoding='utf-8') as f:
        contenido = json.load(f)
    if isinstance(contenido, dict):
        return contenido, 'dict'
    elif isinstance(contenido, list):
        return contenido, 'list'
    else:
        return contenido, type(contenido).__name__

def guardar_contenido(path, contenido):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(contenido, f, indent=4, ensure_ascii=False)

def crear_campos_dinamicos(manager, pos_x, pos_y, campos_def):
    entradas = {}
    labels = {}
    campos = list(campos_def.keys())
    for i, campo in enumerate(campos):
        labels[campo] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((pos_x, pos_y + i*60), (300, 25)),
            text=campo,
            manager=manager
        )
        
        entradas[campo] = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((pos_x, pos_y + i*60 + 25), (300, 30)),
            manager=manager
        )
    
    return entradas, labels

def ventana_gestor_datos(screen):
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    SCREEN_RES = (SCREEN_WIDTH, SCREEN_HEIGHT)
    
    pygame.display.set_caption(TITULO_JUEGO)
    
    try:
        manager = pygame_gui.UIManager(SCREEN_RES)
    except FileNotFoundError:
        manager = pygame_gui.UIManager(SCREEN_RES)
        try:
            alternative_font = pygame.font.SysFont('arial', 14)
            manager.get_theme().set_font_for_element('label', alternative_font)
            manager.get_theme().set_font_for_element('button', alternative_font)
            manager.get_theme().set_font_for_element('text_entry_line', alternative_font)
            manager.get_theme().set_font_for_element('text_box', alternative_font)
            manager.get_theme().set_font_for_element('drop_down_menu', alternative_font)
        except Exception:
            print("No se pudo establecer fuente alternativa")

    background = pygame.Surface(SCREEN_RES)
    background.fill(pygame.Color('#DDDDDD'))

    # ───────────────────────────── UI ELEMENTOS FIJOS ──────────────────────────────
    archivo_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((50, 30), (200, 25)),
        text="Seleccionar archivo:",
        manager=manager
    )
    
    archivo_selector = pygame_gui.elements.UIDropDownMenu(
        options_list=list(ARCHIVOS_JSON.keys()),
        starting_option='Usuarios',
        relative_rect=pygame.Rect((50, 55), (200, 30)),
        manager=manager
    )

    clave_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((50, 100), (200, 25)),
        text="ID o clave:",
        manager=manager
    )
    
    entrada_clave = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((50, 125), (300, 30)),
        manager=manager
    )

    boton_agregar = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((400, 55), (150, 40)),
        text="Agregar",
        manager=manager
    )

    boton_eliminar = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((400, 105), (150, 40)),
        text="Eliminar",
        manager=manager
    )

    boton_buscar = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((400, 155), (150, 40)),
        text="Buscar",
        manager=manager
    )

    boton_ver_todo = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((400, 205), (150, 40)),
        text="Ver Todo",
        manager=manager
    )
    
    boton_cerrar_sesion = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((400, 255), (150, 40)),
        text="Cerrar sesión",
        manager=manager
    )

    salida_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((50, 470), (200, 25)),
        text="Resultados:",
        manager=manager
    )
    
    salida_texto = pygame_gui.elements.UITextBox(
        html_text='',
        relative_rect=pygame.Rect((50, 495), (500, 160)),
        manager=manager
    )

    # ───────────────────────────── CAMPOS DINÁMICOS ──────────────────────────────
    campos_dinamicos = None
    etiquetas_dinamicas = None
    campos_container = pygame.Rect(50, 170, 300, 200)
    
    campos_dinamicos, etiquetas_dinamicas = crear_campos_dinamicos(
        manager, campos_container.x, campos_container.y, 
        CAMPOS_POR_ARCHIVO['Usuarios']['campos']
    )

    # ───────────────────────────── BUCLE PRINCIPAL ─────────────────────────────
    clock = pygame.time.Clock()
    running = True

    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == archivo_selector:
                raw = archivo_selector.selected_option
                nuevo_archivo = raw[0] if isinstance(raw, tuple) else raw
                archivo_selector.selected_option = nuevo_archivo
                
                if campos_dinamicos:
                    for campo in campos_dinamicos.values():
                        campo.kill()
                    for etiqueta in etiquetas_dinamicas.values():
                        etiqueta.kill()
                
                if nuevo_archivo in CAMPOS_POR_ARCHIVO:
                    campos_dinamicos, etiquetas_dinamicas = crear_campos_dinamicos(
                        manager, campos_container.x, campos_container.y, 
                        CAMPOS_POR_ARCHIVO[nuevo_archivo]['campos']
                    )

            # ──────────────── VALIDACIÓN DE CAMPOS VACÍOS AÑADIDA AQUÍ ────────────────
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                opcion_raw = archivo_selector.selected_option
                opcion = opcion_raw[0] if isinstance(opcion_raw, tuple) else opcion_raw
                
                ruta_archivo = ARCHIVOS_JSON[opcion]
                asegurarse_archivo(ruta_archivo)

                clave = entrada_clave.get_text().strip()

                try:
                    datos, tipo = cargar_contenido(ruta_archivo)
                except json.JSONDecodeError as e:
                    salida_texto.set_text(f'Error leyendo JSON: {e}')
                    datos, tipo = None, None
                except Exception as e:
                    salida_texto.set_text(f'Error abriendo "{ruta_archivo}": {e}')
                    datos, tipo = None, None

                if datos is None:
                    continue

                # AGREGAR (con validación de campos vacíos)
                if event.ui_element == boton_agregar:
                    # Verificar clave vacía
                    if not clave:
                        salida_texto.set_text("Error: El campo 'ID o clave' no puede estar vacío")
                        continue
                    
                    tipo_archivo = CAMPOS_POR_ARCHIVO.get(opcion, {}).get('tipo')
                    campos_def = CAMPOS_POR_ARCHIVO[opcion]['campos']
                    
                    if tipo_archivo == 'dict_simple':  # Usuarios
                        # Verificar campo vacío
                        campo = list(campos_def.keys())[0]
                        tipo_dato = campos_def[campo]
                        valor = campos_dinamicos[campo].get_text().strip()
                        
                        if not valor:
                            salida_texto.set_text(f'Error: el campo {campo} no puede estar vacío' )
                            continue
                        datos[clave] = convertir_tipo(valor, tipo_dato)
                        guardar_contenido(ruta_archivo,datos)
                        salida_texto.set_text(f"Usuario agregado: {clave} - {valor}" )
                        
                        
                    elif tipo_archivo == 'objeto':  # Otros archivos
                        nuevo_objeto = {}
                        campos_vacios = []
                        
                        # Verificar todos los campos
                        for campo,tipo_dato in campos_def.items():
                            valor_campo = campos_dinamicos[campo].get_text().strip()
                            if not valor_campo:
                                campos_vacios.append(campo)
                                continue
                            nuevo_objeto[campo] = convertir_tipo(valor_campo,tipo_dato)
                        
                        # Mostrar error si hay campos vacíos
                        if campos_vacios:
                            salida_texto.set_text(f"Error: Campos vacíos: {', '.join(campos_vacios)}")
                            continue
                            
                        datos[clave] = nuevo_objeto
                        guardar_contenido(ruta_archivo, datos)
                        salida_texto.set_text(f'Objeto agregado para {clave}:\n{json.dumps(nuevo_objeto, indent=2)}')
                        
                    elif tipo == 'list':
                        salida_texto.set_text('Operación no soportada para listas')
                    else:
                        salida_texto.set_text(f'Tipo no soportado: {tipo}')

                # ELIMINAR (con validación de clave vacía)
                elif event.ui_element == boton_eliminar:
                    if not clave:
                        salida_texto.set_text("Error: El campo 'ID o clave' no puede estar vacío")
                        continue
                        
                    if tipo == 'dict':
                        if clave in datos:
                            del datos[clave]
                            guardar_contenido(ruta_archivo, datos)
                            salida_texto.set_text(f'Eliminado: {clave}')
                        else:
                            salida_texto.set_text('Clave no encontrada')
                    elif tipo == 'list':
                        salida_texto.set_text('Operación no soportada para listas')
                    else:
                        salida_texto.set_text(f'Tipo no soportado: {tipo}')

                # BUSCAR (con validación de clave vacía)
                elif event.ui_element == boton_buscar:
                    if not clave:
                        salida_texto.set_text("Error: El campo 'ID o clave' no puede estar vacío")
                        continue
                        
                    if tipo == 'dict':
                        if clave in datos:
                            resultado = datos[clave]
                            if isinstance(resultado, dict):
                                texto = json.dumps(resultado, indent=2)
                                salida_texto.set_text(f'Resultado para {clave}:\n{texto}')
                            else:
                                salida_texto.set_text(f'{clave}: {resultado}')
                        else:
                            salida_texto.set_text('Clave no encontrada')
                    elif tipo == 'list':
                        salida_texto.set_text('Operación no soportada para listas')
                    else:
                        salida_texto.set_text(f'Tipo no soportado: {tipo}')
                
                # VER TODO (no requiere validación)
                elif event.ui_element == boton_ver_todo:
                    if tipo == 'dict':
                        claves = list(datos.keys())
                        texto_salida = f'Claves en {opcion}:\n' + '\n'.join(claves)
                        salida_texto.set_text(texto_salida)
                    elif tipo == 'list':
                        salida_texto.set_text('Operación no soportada para listas')
                    else:
                        salida_texto.set_text(f'Tipo no soportado: {tipo}')
                
                # CERRAR SESIÓN (no requiere validación)
                elif event.ui_element == boton_cerrar_sesion:
                    return "LOGOUT"

            manager.process_events(event)

        manager.update(time_delta)
        screen.blit(background, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()

# Bloque para ejecutar independientemente
if __name__ == "__main__":
    SCREEN_WIDTH, SCREEN_HEIGHT = 920, 690
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Gestor de Datos JSON (Modo Independiente)")

    try:
        result = ventana_gestor_datos(screen)
        if result == "LOGOUT":
            from menu import menuPrincipal
            menuPrincipal(screen)
    except FileNotFoundError:
        pygame.font.init()
        ventana_gestor_datos(screen)

    pygame.quit()
    sys.exit()