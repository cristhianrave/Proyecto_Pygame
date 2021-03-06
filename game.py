import pygame as pg
from pygame.locals import *
import sys
from entities import *
from random import randint
from planetas import *
from ranking import *


FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (30, 186, 22)

class Game:
    clock = pg.time.Clock()
    nivel = 1
    puntuacion = 0

    def __init__(self):
        pg.font.init()
      
        self.screen = pg.display.set_mode((800,600))
        pg.display.set_caption ('The Quest')
        self.background_image = pg.image.load('resources/images/fondo_nave.jpg').convert()
        self.font = pg.font.Font('resources/fonts/PressStart.ttf', 22)
        self.fonty = pg.font.Font('resources/fonts/PressStart.ttf', 26)
        self.fonty2 = pg.font.Font('resources/fonts/PressStart.ttf', 62)
        
        self.player = Nave()
        self.asteroide = Asteroide()
        self.planeta = Planeta()
        self.nave_rotate = Nave_rotate()
        self.ranking = Ranking()
       
        self.asteroidesGroup = pg.sprite.Group()
        self.naveGroup = pg.sprite.Group()
        self.planetaGroup = pg.sprite.Group()
        self.nave_rotateGroup = pg.sprite.Group()

        self.asteroidesGroup.add(self.asteroide)
        self.naveGroup.add(self.player)

        self.num_asteroides_creados = 0
        self.asteroides_en_pantalla = 15
        self.tiempo_para_crear_asteroide = FPS*10
        self.crear_asteroide = FPS*8.       

 
    def crear_asteroides(self, dt): 
  
        self.tiempo_para_crear_asteroide += dt
        if  self.tiempo_para_crear_asteroide > self.crear_asteroide:
            self.asteroide = Asteroide(randint(780, 840), randint(10, 550))
            self.asteroide.speed = (randint(1, 2))
            self.asteroidesGroup.add(self.asteroide)
            self.num_asteroides_creados += 1
            self.tiempo_para_crear_asteroide = 0 
     
    def asteroide_nivel_2(self, dt):       
        self.asteroide1 = Asteroide(randint(780, 840), randint(10, 550))
        self.asteroide1.speed = (randint(2, 4))
        self.asteroidesGroup.add(self.asteroide1)
        self.num_asteroides_creados += 1


    def text(self):
        self.marcador_vidas = self.font.render('Vidas:', True, GREEN)
        self.marcador_score = self.font.render('Puntos:', True, GREEN)
        self.marcador_nivel = self.font.render('Nivel:', True, GREEN)
        self.marcador_vidas_num = self.font.render(str(self.player.vidas), True, RED)
        self.marcador_score_num = self.font.render(str(self.puntuacion), True, RED)
        self.marcador_nivel_num = self.font.render(str(self.nivel), True, RED)
        self.gameOver_text1 = self.fonty2.render('Game Over', True, RED)
        self.gameOver_text2 = self.font.render('"Space" para guardar', True, WHITE)
        self.gameOver_text3 = self.font.render('"Escape" para volver al Menu.', True, WHITE)
        

    def salir_juego(self):
        pg.quit()
        sys.exit()

    def gameOver(self,dt):
        self.handleEvents2(dt)

        self.screen.blit(self.gameOver_text1,(130, 150))
        self.screen.blit(self.gameOver_text2,(90, 400))
        self.screen.blit(self.gameOver_text3,(90, 450))

    def handleEvents2(self,dt):
        for event in pg.event.get():
            if event.type == QUIT:
                self.salir_juego()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.mixer.music.stop()
                    self.bucle_game = False 
                if event.key == K_SPACE:
                    self.ranking.mostrar_ranking(self.puntuacion)
                    pg.mixer.music.stop()
                    self.bucle_game = False

    def handleEvents(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.salir_juego()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.player.go_up()
                if event.key == K_DOWN:
                    self.player.go_down()
                if event.key == K_ESCAPE:
                    self.bucle_game = False
    
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[K_UP]:
            self.player.go_up()
        if keys_pressed[K_DOWN]:
            self.player.go_down()

    def nivel_2(self,dt):
        if  self.puntuacion  > 200  :
            self.nivel = 2  
            if self.cant_asteroides_creados < self.asteroides_en_pantalla:                
                self.asteroide_nivel_2(dt)

    def nivel_3(self,dt):
        if  self.puntuacion  > 300  :
            self.nivel = 3  
            
            if self.cant_asteroides_creados < self.asteroides_en_pantalla:                
                self.asteroide_nivel_2(dt)

    def nivel_4(self,dt):
        if  self.puntuacion  > 400  :
            self.nivel = 4 
            
            if self.cant_asteroides_creados < self.asteroides_en_pantalla:                
                self.asteroide_nivel_2(dt)

    def intro_planeta(self,dt):  
        
        self.num_asteroides_creados = 0
        self.naveGroup.empty()
        self.screen.blit(self.background_image, (0,0))
        self.screen.blit(self.marcador_nivel,(10, 10))
        self.screen.blit(self.marcador_nivel_num,(150, 10))
        self.screen.blit(self.marcador_vidas,(300, 10))
        self.screen.blit(self.marcador_vidas_num,(440, 10))
        self.screen.blit(self.marcador_score,(540, 10))
        self.screen.blit(self.marcador_score_num,(720, 10))

        self.asteroidesGroup.update(dt)      
        self.asteroidesGroup.draw(self.screen)
        self.planetaGroup.add(self.planeta)      
        self.planetaGroup.update(dt)
        self.planetaGroup.draw(self.screen)
        self.nave_rotateGroup.add(self.nave_rotate)
        self.nave_rotateGroup.update(dt)
        self.nave_rotateGroup.draw(self.screen)
        self.handleEvents2(dt)

            

    def renderiza(self,dt):

        self.screen.blit(self.background_image, (0,0))
        self.screen.blit(self.marcador_nivel,(10, 10))
        self.screen.blit(self.marcador_nivel_num,(150, 10))
        self.screen.blit(self.marcador_vidas,(300, 10))
        self.screen.blit(self.marcador_vidas_num,(440, 10))
        self.screen.blit(self.marcador_score,(570, 10))
        self.screen.blit(self.marcador_score_num,(725, 10))

        self.asteroidesGroup.update(dt)
        self.naveGroup.update(dt)

        self.asteroidesGroup.draw(self.screen)
        self.naveGroup.draw(self.screen)


    def bucle_partida(self,dt):

        self.handleEvents()
        self.player.comprobar_colision(self.asteroidesGroup)

        self.cant_asteroides_creados = len(self.asteroidesGroup)
        if self.cant_asteroides_creados < self.asteroides_en_pantalla:
            self.crear_asteroides(dt)
        
        if  self.num_asteroides_creados > self.asteroides_en_pantalla:
            self.puntuacion = self.num_asteroides_creados * 10

        self.nivel_2(dt)
        self.nivel_3(dt)
        self.nivel_4(dt)
        
        self.text()
        self.renderiza(dt)

    def mainloop_juego(self):
        self.bucle_game = True
        while self.bucle_game:
            dt = self.clock.tick(FPS)

            if self.player.vidas > 0 and self.puntuacion < 500:
                self.bucle_partida(dt)

            if self.player.vidas == 0:
                self.gameOver(dt)

            if self.puntuacion == 500 and self.player.vidas > 0:
                self.intro_planeta(dt)
            
            
            pg.display.flip()
