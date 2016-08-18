"""
[main.py]
Autor: Sebastian Borquez G - COR2016
Fecha: 08/2016
Descripcion: Checkpoint. Muestra cronometro generado en un Arduino a travez de PyGame.
    
"""

from cronometro.arduinoserial import Arduino
from cronometro.display import *
import pygame
from pygame.locals import *
import sys


class Menu(Scene):

    """Ventana inicial.

    Presenta las opciones para conectarse, comenzar o salir del programa.

    """

    def __init__(self, MainFrame, Escenas):
        Scene.__init__(self, MainFrame)

        # Teclas presionadas.
        self.pressed = {pygame.K_DOWN: False,
                        pygame.K_UP: False,
                        pygame.K_SPACE: False}

        # Escenas disponibles para cambiar.
        self.escenas = Escenas

        # Opcion seleccionada.
        self.opciones = 0

        # Estados del Arduino.
        self.arduino_connected = "not tried"
        self.cronometro = None

        # Datos para dibujar.
        self.bg = load_image("recursos/imagenes/background1.jpg")
        self.mensaje = "Conectar Arduino"
        self.punterox = WIDTH/4
        self.punteroy = 6*HEIGHT/8

    def on_update(self):

        # En caso de conectarse, cambiar a la escena del cronometro.
        if self.arduino_connected == "ok":
            self.escenas["Timer"].cronometro = self.cronometro
            self.cronometro = None
            self.arduino_connected = "not tried"
            self.mensaje = "Conectar Arduino"
            self.director.change_scene(self.escenas["Timer"])

        # En caso de no encontrar ningun Arduino.
        if self.arduino_connected == "fail":
            self.mensaje = "Conectar Arduino - Fail!"

        # Datos para dibujar el puntero.
        if self.opciones:
            self.punteroy = 7*HEIGHT/8
        else:
            self.punteroy = 6*HEIGHT/8

    def on_event(self):
        """ Si se selecciona en conectar o en salir hacer algo"""

        # Intecambio entre opciones a travez del teclado.
        if self.once_pressed(pygame.K_DOWN):
            self.opciones = abs(self.opciones-1)

        if self.once_pressed(pygame.K_UP):
            self.opciones = (self.opciones + 1) % 2

        # Seleccion de opcion a travez del teclado.
        if self.once_pressed(pygame.K_SPACE):
            if self.opciones == 0:
                self.cronometro = Arduino(9600)
                if self.cronometro.conectado:
                    self.arduino_connected = "ok"
                else:
                    self.arduino_connected = "fail"
            if self.opciones == 1:
                self.director.quit()

    def on_draw(self, screen):
        """ Informacion desplegada en pantalla."""

        # Fondo.
        screen.blit(self.bg, (0, 0))

        # Puntero.
        pygame.draw.circle(
            screen, (0, 0, 0), (self.punterox, self.punteroy), 10)

        # Textos.
        opcion1 = fuente.render(self.mensaje, 1, (0, 0, 0))
        opcion2 = fuente.render("Salir", 1, (0, 0, 0))
        screen.blit(opcion1, (20+WIDTH/4, 6*HEIGHT/8 - 10))
        screen.blit(opcion2, (20+WIDTH/4, 7*HEIGHT/8 - 10))

    def once_pressed(self, key):
        """ Detecta si una tecla fue presionada una vez."""
        if pygame.key.get_pressed()[key] and not self.pressed[key]:
            self.pressed[key] = True
            return True
        if not pygame.key.get_pressed()[key]:
            self.pressed[key] = False
        return False


class Timer(Scene):

    """Display de cronometro"""

    def __init__(self, MainFrame, Escenas):
        Scene.__init__(self, MainFrame)

        # Escenas disponibles para intercambiar.
        self.escenas = Escenas

        # Representacion de la placa Arduino
        self.cronometro = None

        # Datos para Dibujar
        self.bg = load_image("recursos/imagenes/background2.jpg")
        # Tiempo
        self.runningtime = "Stand by"
        self.backtime = self.runningtime
        self.vuelta1 = "-"
        self.vuelta2 = "-"

        # Estados de la escena.
        self.pressed = False
        self.cambiar = False

    def on_update(self):
        """ Actualizacion logica de la escena"""

        # Cambiar a la pantalla principal.
        if self.cambiar:
            self.cambiar = False
            self.director.change_scene(self.escenas["Menu"])

        # Actualizar datos del cronometro.
        else:
            self.runningtime = self.cronometro.getdata()
            if len(self.runningtime) == 0:
                self.runningtime = self.backtime
            else:
                self.backtime = self.runningtime
    def on_event(self):
        """ Detecta si se presiona algun boton."""

        # Cambiar estado de escena para volver a la escena principal.
        # Borrar puntero a Arduino.
        if self.once_pressed(pygame.K_BACKSPACE):
            self.cambiar = True
            self.cronometro.kill()
            self.cronometro = None

    def on_draw(self, screen):
        """ Informacion desplegada en pantalla."""

        # Fondo.
        screen.blit(self.bg, (0, 0))

        # Cronometro.
        try:
            tiempo = int(self.runningtime)
            tiempo = cambiar_tiempo(tiempo)
        except:
            tiempo = self.runningtime
        running = fuentecronometro.render(tiempo, 1, (255, 255, 255))
        screen.blit(running, (WIDTH/5, HEIGHT/3))

        # Tiempos de vueltas.
        tiempo1 = fuente.render("> 1: " + self.vuelta1, 1, (255, 255, 255))
        tiempo2 = fuente.render("> 2: " + self.vuelta2, 1, (255, 255, 255))

        screen.blit(tiempo1, (WIDTH/3, 5*HEIGHT/8))
        screen.blit(tiempo2, (WIDTH/3, 6*HEIGHT/8))


    def once_pressed(self, key):
        """ Detecta si una tecla fue presionada una vez."""

        if pygame.key.get_pressed()[key] and not self.pressed:
            self.pressed = True
            return True
        if not pygame.key.get_pressed()[key]:
            self.pressed = False
        return False

def cambiar_tiempo(tiempo):
    decisegundos = str(tiempo%10)
    segundos = (tiempo/10)%100
    minutos = tiempo/1000
    if segundos/10 == 0:
        segundos = "0" + str(segundos) 
    if minutos/10 == 0:
        minutos = "0" + str(minutos) 

    cronometro = "{0}:{1}.{2}".format(minutos,segundos,decisegundos)
    return cronometro

if __name__ == '__main__':
    Main = MainFrame(title="Cronometro")
    Escenas = dict()
    Escenas["Menu"] = Menu(Main, Escenas)
    Escenas["Timer"] = Timer(Main, Escenas)
    Main.change_scene(Escenas["Menu"])
    Main.loop()
