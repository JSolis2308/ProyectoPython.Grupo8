# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 17:47:03 2021

@author: sergi
"""
#!/usr/bin/python3

#Sergio Camacho B91476
#Johan Solis
#Mario

#Proyecto Python Programación
#Este programa consistirá en un Tetris

import pygame
import random


"""
El programa se enfocará en una cuadrícula de juego
que tendrá sus propias coordenadas [x] [y], y una clase Pieza
que guardará las diferentes piezas del juego, estas se van a representar
usando listas de listas(porque hay diferentes rotaciones de cada pieza)
el 0 indicará el espacio en el que se pintarán las coordenadas 
de la ventana principal del juego, y demás funciones que le darán vida
al juego...estas se irán explicando conforme se declaren
"""

pygame.font.init()
# Globales:
ancho_total = 800
altura_total = 700
ancho_juego = 300  # 10 cuadrados con ancho de 35 px
altura_juego = 600  # 20 cuadrados con 35 px de altura
tamano_cuadrados = 30
# Para corregir colisiones con el área de juego agregaré aquí 2 variables:
esq_sup_izq_x = (ancho_total - ancho_juego) // 2
esq_sup_izq_y = altura_total - altura_juego



# FORMAS:

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

formas = [S, Z, I, O, J, L, T]
colores_RGB = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# los índices indican cuál color le pertenece a cada forma


class Pieza(object):  # * 
    def __init__(self, x, y, forma):
        self.x = x
        self.y = y
        self.forma = forma
        self.color = colores_RGB[formas.index(forma)]
        # se extrae el color que le corresponda a la forma
        self.rotacion = 0
        
        # esta clase solo necesita el inicializador

def crear_cuadricula(pos_ocupadas={}):  # *
    # esta función crea la cuadricula principal de posiciones virtuales del juego,
    # será reutilizada en la función principal y por eso recibe un parámetro 
    # pos_ocupadas en el que se fijarán las piezas que ya llegaron a fondo
    cuadricula = [[(255,255,255) for j in range(10)] for i in range(20)]
    
    for i in range(len(cuadricula)):
        for j in range(len(cuadricula[i])):
            if (j, i) in pos_ocupadas:
                colortemp = pos_ocupadas[(j,i)]
                cuadricula[i][j] = colortemp
                # este for lo que hace es revisar las llaves de pos_ocupadas y si
                # hay una posicion ya guardada se colorea del color de esa pieza
    return cuadricula

def formatear_forma(forma):
    # esta funcion transforma las listas de 0s y puntos en posiciones de la cuadricula para la funcion crear_cuadricula
    posiciones = []
    formato = forma.forma[forma.rotacion % len(forma.forma)]
    # el modulo viene de que dependiendo de self.rotacion se escoge cual de las rotaciones mostrar (ej: 4%4 = 0, es decir se muestra la rotación 0, la original) 
    for i, linea in enumerate(formato):
        fila = list(linea)
        for j, columna in enumerate(fila):
            if columna == '0':
                posiciones.append((forma.x + j, forma.y + i))

    for i, pos in enumerate(posiciones):
        posiciones[i] = (pos[0] - 2, pos[1] - 4)
        # esas constantes se encargan de quitar los puntos de la lista para solo contar los 0s

    return posiciones

def mov_val(forma, cuadricula):
    # significa movimiento válido
    # esta función se va a encargar de revisar si algún movimiento o colisión es válida o no
    pos_aceptadas = []
    for i in range(20):
        for j in range(10):
            if cuadricula[i][j] == (255,255,255):
                # básicamente lo que esta función revisa es que el espacio al que quiere moverse es blanco
                # y entonces lo aprueba
                pos_aceptadas.append((j,i))
    
    formateada = formatear_forma(forma)

    for pos in formateada:
        if pos not in pos_aceptadas:
            if pos[1] > -1: 
                # este if es porque usualmente las piezas empezarán desde arriba de la ventana principal
                return False
    return True
  
def perder(posiciones):
    # esta función es bastante simple, revisa si alguna pieza ya llegó al tope
    for pos in posiciones:
        x, y = pos
        if y < 1:
            return True 
            # perdiste
    return False 
    # estás vivo        

def get_forma():
    # retorna una pieza al azar de las diferentes formas disponibles
    return Pieza(5, 0, random.choice(formas))
    # si se fijan bien, la x es 5 porque estamos trabajando con coordenadas de la cuadrícula

def dibujar_cuadricula(superficie, cuadricula):
    # se toma como referencia la esquina superior izquierda y esta función
    # lo que hace es crear las líneas divisorias de la cuadrícula del juego
    px = esq_sup_izq_x
    py = esq_sup_izq_y

    for i in range(len(cuadricula)):
        # por cada fila se dibuja la linea desde la x de la esquina hasta el otro lado de la ventana de juego
        pygame.draw.line(superficie, (128,128,128), (px, py + i*tamano_cuadrados), (px + ancho_juego, py + i*tamano_cuadrados))
        for j in range(len(cuadricula[i])):
        # y para la y se itera para multiplicar la distancia de cada cuadrado para cada una de las divisiones           
            pygame.draw.line(superficie, (128, 128, 128), (px + j*tamano_cuadrados, py),(px + j*tamano_cuadrados, py + altura_juego))

def dibujar_textoenelmedio(texto, size, color, superficie):  
    # esta función servirá para cuando pierdas y actualmente el menú principal la usa
    # crea un texto en el medio de la pantalla
    pygame.font.init()
    font = pygame.font.SysFont('timesnewroman', size)
    despedida = font.render(texto, 1, color)
    superficie.blit(despedida, (esq_sup_izq_x + ancho_juego/2 - (despedida.get_width()/2), esq_sup_izq_y + altura_juego/2 - despedida.get_height()))
                                
def borrar_fila(cuadricula, ocupadas):
    # esta función fue la más complicada de hacer, se encarga de borrar las filas
    # que ya se hayan llenado con piezas, de mover todo el resto de la cuadrícula hacia abajo, 
    # y de agregar una nueva fila arriba, para esto se declara la variable incremento
    incremento = 0
    for i in range(len(cuadricula) - 1, -1, -1):
        fila = cuadricula[i]
        if (255,255,255) not in fila:
            # al no haber ya más colores blancos en la fila, significa que fue completada
            incremento += 1
            index = i # este index nos dice cuál fila hay que borrar y será útil después
            for j in range(len(fila)):
                try:
                    del ocupadas[(j,i)]
                except:
                    continue
    
    # ahora para mover lo demás
    if incremento > 0:
        # es decir, si alguna fila fue borrada
        # se busca en una lista ordenada de las llaves de ocupadas, de la última a la primera
        for key in sorted(list(ocupadas), key=lambda s: s[1]) [::-1]:
            x, y = key
            if y < index:
                # para no mover las filas debajo de la que se eliminó
                newkey = (x, y + incremento)
                ocupadas[newkey] = ocupadas.pop(key)
        # la razón por la que se itera en reversa es porque es más fácil para la memoria y además
        # se podría cometer un error en el que se mueve una fila hacia abajo que tuviera colores
        # en la misma x, de esta forma sobreescribiendo a la de abajo, es mejor ir en reversa
    return incremento
            
            

def dibujar_pieza_sig(forma, superficie):
    # dibuja la pieza siguiente
    font = pygame.font.SysFont('timesnewroman', 30)
    mensaje = font.render('Siguiente pieza', 1, (0,0,0))
    
    px = esq_sup_izq_x + ancho_juego + 20
    py = esq_sup_izq_y + altura_juego/2 - 100
    formato = forma.forma[forma.rotacion % len(forma.forma)]
    
    # mismo código que en formatear_forma pero esta vez dibuja
    for i, linea in enumerate(formato):
        fila = list(linea)
        for j, columna in enumerate(fila):
            if columna == '0':
                pygame.draw.rect(superficie, forma.color, (px + j*tamano_cuadrados, py + i*tamano_cuadrados, tamano_cuadrados, tamano_cuadrados), 0)
    
    superficie.blit(mensaje, (px + 10, py - 30))
    

def dibujar_ventana(superficie, cuadricula, puntaje=0):
    # esta función crea toda la pantalla del juego básicamente
    superficie.fill((255,255,255)) # superficie
    pygame.font.init()
    font = pygame.font.SysFont('timesnewroman', 60)
    titulo = font.render('Tetris', 1, (0,0,0)) # título
    superficie.blit(titulo, (esq_sup_izq_x + ancho_juego / 2 - (titulo.get_width() / 2), 20)) # título
    
    # espacio para demás cosas que se quieran agregar a la pantalla
    font = pygame.font.SysFont('timesnewroman', 30)
    puntuacion = font.render('Puntuación: ' + str(puntaje), 1, (0,0,0)) # título
    px = esq_sup_izq_x + ancho_juego + 20
    py = esq_sup_izq_y + altura_juego/2 - 100
    superficie.blit(puntuacion, ((px + 10), (py + 150))) # puntaje
    
    for i in range(len(cuadricula)):
        for j in range(len(cuadricula[i])):
            pygame.draw.rect(superficie, cuadricula[i][j], ((esq_sup_izq_x + j*tamano_cuadrados), (esq_sup_izq_y + i*tamano_cuadrados), tamano_cuadrados, tamano_cuadrados), 0)
            # estos son cada uno de los cuadrados del juego pero físicamente
    pygame.draw.rect(superficie, (255, 0, 0), (esq_sup_izq_x, esq_sup_izq_y, ancho_juego, altura_juego), 5)
    # este es el borde de la ventana principal del juego
    
    dibujar_cuadricula(superficie, cuadricula)
    
def main(vent):
    # función principal del juego
    # se declaran las variables principales
    pos_ocupadas = {} # ya se ha mostrado varias veces
    cuadricula = crear_cuadricula(pos_ocupadas) # esta también
    cambiar_pieza = False # este booleano nos indica si se necesita cambiar pieza
    active = True # variable para loopear el juego
    pieza_actual = get_forma()
    pieza_sig = get_forma()
    reloj = pygame.time.Clock() # un reloj
    tiempo_caida = 0 # esto cambiará gracias al reloj
    vel_caida = 0.25
    # vel_caida nada más servirá para cuando tiempo_caida llegue a 0.25 mover la pieza hacia abajo automáticamente
    puntaje = 0 # puntaje cambia de acuerdo con las filas que se borren
    
    while active:
        cuadricula = crear_cuadricula(pos_ocupadas)
        # se tiene que poner esto acá porque hay que revisar constantemente pos_ocupadas
        tiempo_caida += reloj.get_rawtime() # retorna el tiempo transcurrido gracias al tick
        reloj.tick()
        
        if tiempo_caida/1000 > vel_caida: # ticks de reloj estan en ms
            # vel_caída no es una velocidad como tal, sino una marca de tiempo
            # para que las piezas se muevan solas con el tiempo
            tiempo_caida = 0
            pieza_actual.y += 1
            if((mov_val(pieza_actual, cuadricula) is False) and (pieza_actual.y > 0)):
                # si un movimiento del juego llega a ser inválido la única explicación es
                # que ya se tocó suelo, por ende hay que fijar la pieza y cambiarla
                pieza_actual.y -= 1
                cambiar_pieza = True # este segmento está más abajo
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                pygame.display.quit()
            
            # Teclas (movimiento será con wasd o flechas):
            if event.type == pygame.KEYDOWN:
                # se usa mov_val para validar cada tecla
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    pieza_actual.x -= 1
                    if mov_val(pieza_actual, cuadricula) is False:
                        pieza_actual.x += 1
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    pieza_actual.x += 1
                    if mov_val(pieza_actual, cuadricula) is False:
                        pieza_actual.x -= 1
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    pieza_actual.y += 1
                    if mov_val(pieza_actual, cuadricula) is False:
                        pieza_actual.y -= 1
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    pieza_actual.rotacion += 1
                    if mov_val(pieza_actual, cuadricula) is False:
                        pieza_actual.rotacion -= 1
                if event.key == pygame.K_SPACE:
                    vel_caida -= 0.05 # aumenta la velocidad de caída
                if event.key == pygame.K_BACKSPACE:
                    vel_caida += 0.05 # reduce la velocidad de caída
                if event.key == pygame.K_ESCAPE:
                    active = False # se sale del juego
                    
        pos_forma = formatear_forma(pieza_actual)
        
        for i in range(len(pos_forma)):
            # esto lo que hace es colorear donde esté la pieza
            # así parece que en serio hay una figura de pygame moviéndose cuando en realidad
            # son solo cuadrados coloreándose
            x, y = pos_forma[i]
            if y > -1:
                cuadricula[y][x] = pieza_actual.color
                
        if cambiar_pieza is True:
            # cuando hay que cambiar de pieza se fija la posición de la pieza actual para que quede grabada permanentemente en la cuadrícula 
            for pos in pos_forma:
                p = (pos[0], pos[1])
                pos_ocupadas[p] = pieza_actual.color
            pieza_actual = pieza_sig
            pieza_sig = get_forma()
            cambiar_pieza = False
            puntaje += borrar_fila(cuadricula, pos_ocupadas) * 25 
            # la revisión de si se completó una fila
            # se hace hasta que se termine con la pieza actual
            # y se suma al puntaje
        
        dibujar_ventana(vent, cuadricula, puntaje)
        dibujar_pieza_sig(pieza_sig, vent)
        pygame.display.update()

        if perder(pos_ocupadas) is True:
            # esto se accesa cuando se pierde la partida
            # usa la función de texto en el medio para imprimir PERDISTE :P
            # luego espera un poco para que se pueda leer y luego termina la partida
            dibujar_textoenelmedio('PERDISTE :P', 80, (0,0,0), vent)
            pygame.display.update()
            pygame.time.delay(1500)
            active = False

def main_menu(vent):
    # main menu pendiente
    activo = True
    while activo:
        # loop de main_menu
        # de momento pide una tecla para iniciar que no sea ESC porque con esa se sale del juego
        vent.fill((0,0,0))
        dibujar_textoenelmedio('Menú pendiente xd estripen algo excepto ESCAPE', 40, (255,255,255), vent)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                activo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    activo = False
                else:
                    main(vent)

vent = pygame.display.set_mode((ancho_total, altura_total))
pygame.display.set_caption('Tetris')
main_menu(vent)
pygame.display.quit()