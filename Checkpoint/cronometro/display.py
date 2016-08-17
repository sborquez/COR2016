"""
[display.py]
Autor: Sebastian Borquez G - COR2016
Autor Original: http://razonartificial.com/
Fecha: 08/2016
Descripcion: Mostrar informacion utilizando PyGame.
    
"""

import pygame
from pygame.locals import *
import sys
 
pygame.init()

WIDTH = 852
HEIGHT = 480
FULLSCREEN = True
fuente = pygame.font.Font("recursos/fuentes/PressStart2P.ttf", int(WIDTH*0.02347))
fuentecronometro = pygame.font.Font("recursos/fuentes/PressStart2P.ttf", int(WIDTH*0.082159))
pygame.mouse.set_visible(False)

class MainFrame:
    """Representa la ventana principal del juego.
 
    Mantiene en funcionamiento el juego, se
    encarga de actualizar, dibuja y propagar eventos.
    
    """

    def __init__(self, title, SW=WIDTH, SH=HEIGHT):
        self.screen = pygame.display.set_mode((SW, SH))
        pygame.display.set_caption(title)
        self.scene = None
        self.quit_flag = False
        self.clock = pygame.time.Clock()
        pygame.display.toggle_fullscreen() 
 
    def loop(self):
        "Pone en funcionamiento el juego."
 
        while not self.quit_flag:
            time = self.clock.tick(60)
             
            # Eventos de Salida
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        pygame.display.toggle_fullscreen() 
 
            # detecta eventos
            self.scene.on_event()
 
            # actualiza la escena
            self.scene.on_update()
 
            # dibuja la pantalla
            self.scene.on_draw(self.screen)
            pygame.display.flip()
 
    def change_scene(self, scene):
        "Altera la escena actual."
        self.scene = scene
 
    def quit(self):
        self.quit_flag = True

class Scene:
    """Representa un escena abstracta del videojuego.
 
    Una escena es una parte visible del juego, como una pantalla
    de presentacion o menu de opciones. Tiene que crear un objeto
    derivado de esta clase para crear una escena utilizable."""
 
    def __init__(self, director):
        self.director = director
 
    def on_update(self):
        "Actualizacion logica que se llama automaticamente desde el director."
        raise NotImplementedError
 
    def on_event(self, event):
        "Se llama cuando llega un evento especifico al bucle."
        raise NotImplementedError
 
    def on_draw(self, screen):
        "Se llama cuando se quiere dibujar la pantalla."
        raise NotImplementedError

def load_image(filename, transparent=False):
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
        return image