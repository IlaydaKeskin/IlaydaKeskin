import pygame
from pygame.constants import (QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_SPACE, MOUSEBUTTONDOWN)
import os
from random import *
pygame.mixer.init()

#bildschirm
class Settings(object):
    def __init__(self):
        self.width = 700                                                  
        self.height = 500                                                  
        self.fps = 60                                                       
        self.title = "Grinch the Christmas Destroyer"                                          
        self.image_path = os.path.dirname(os.path.abspath(__file__))        

    def size(self):                                                        
        return (self.width, self.height)   
#spieler
class Grinch(pygame.sprite.Sprite):
    def __init__(self, settings):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.image = pygame.image.load(os.path.join(self.settings.image_path, "grinchhand.png")).convert_alpha() #spielerpng
        self.image = pygame.transform.scale(self.image, (110, 130)) #größe
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top=pygame.mouse.get_pos()
        
    def update(self):
        self.rect.left,self.rect.top=pygame.mouse.get_pos()

#blasen
class Kugeln(pygame.sprite.Sprite):
    def __init__(self, settings):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.size= 8
        self.image = pygame.image.load(os.path.join(self.settings.image_path, "Kugeln.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.left = randint(90,self.settings.width-110-self.size)
        self.rect.top = randint(90,self.settings.height-110-self.size)
        self.grow = randint(1,4)

    def update(self):
        if self.size < 100:
            center = self.rect.center
            self.size += self.grow
            self.image = pygame.image.load(os.path.join(self.settings.image_path, "Kugeln.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = pygame.mask.Mask.get_rect(self.mask)
            self.rect.center = center
#punkte
class punkte():
    def __init__(self, settings):
        self.settings = settings
        self.image = pygame.image.load(os.path.join(self.settings.image_path, "punkteanzeige.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (130, 90))

#spiel
class Spiel(object):
    def __init__(self, pygame, settings):
        self.pygame = pygame #hintergrund
        self.settings = settings
        self.screen = pygame.display.set_mode(settings.size())                                      
        self.pygame.display.set_caption(self.settings.title)                                                
        self.background = self.pygame.image.load(os.path.join(self.settings.image_path, "Tannenbaum.png")).convert()
        self.background = pygame.transform.scale(self.background, (700, 500))                            
        self.background_rect = self.background.get_rect()
        self.Grinch = Grinch(settings) #figuren

        self.points = punkte(settings) 
        self.pointscolor = [0,0,0]                                            # Einstellungen zur Punkte Anzeige
        self.pointsadd = 0
        self.font = pygame.font.Font(None, 35)                                                        
        self.text = self.font.render(str(self.pointsadd), True, self.pointscolor)                     
        self.textRect = self.text.get_rect()                                                            
        self.textRect.center = 28, 6

        self.clock = pygame.time.Clock()
        self.done = False

        self.kugelnspawn = 0

        pygame.mouse.set_visible(False)

        self.all_Kugeln = pygame.sprite.Group() #gruppen für sprites
        self.the_mouse = pygame.sprite.Group()

        self.the_mouse.add(self.Grinch)

        self.ticks = pygame.time.get_ticks()                                        #Zeit berechnung
        self.Nummerierung = 0
        self.spawn= ((pygame.time.get_ticks()-self.ticks)/1000) + self.Nummerierung

        pygame.mouse.set_visible(False) #maus unsichtbar


    
    def run(self):
        while not self.done:                            
            self.clock.tick(self.settings.fps)   
            self.time = (pygame.time.get_ticks()-self.ticks)/1000   
            self.secs = round(self.time, 1)   
            for event in self.pygame.event.get():       
                if event.type == QUIT:                  
                    self.done = True                 
                elif event.type == KEYDOWN:            
                    if event.key == K_ESCAPE:
                        self.done = True

                touchbubble= pygame.sprite.spritecollide(self.Grinch, self.all_Kugeln, False)     # Kollisionserkennung       

                if touchbubble:                                                                     # Bei Kollision wechseln
                    self.Grinch.image = pygame.image.load(os.path.join(self.settings.image_path, "grinchhand2.png")).convert_alpha()
                    self.Grinch.image = pygame.transform.scale(self.Grinch.image, (110, 130))

                if not touchbubble:
                    self.Grinch.image = pygame.image.load(os.path.join(self.settings.image_path, "grinchhand.png")).convert_alpha()
                    self.Grinch.image = pygame.transform.scale(self.Grinch.image, (110, 130))

                if event.type == MOUSEBUTTONDOWN and touchbubble:                                   # bei Kollision löschen
                    pygame.sprite.spritecollide(self.Grinch, self.all_Kugeln, True)
                    self.pointsadd += 1
                    self.text = self.font.render(str(self.pointsadd), True, self.pointscolor)
                    self.kugelnspawn -= 1

            self.update()                               
            self.draw()                                
 
    def draw(self):
        self.screen.blit(self.background, self.background_rect)
        self.all_Kugeln.draw(self.screen)
        self.screen.blit(self.points.image,(2,4))
        self.screen.blit(self.text, self.textRect.center)
        self.the_mouse.draw(self.screen)
        self.pygame.display.flip()    

    def update(self):
        self.morebubbles()
        self.all_Kugeln.update() 
        self.the_mouse.update()

    def morebubbles(self):                                  # Berechnung und Funkiton zum Blasen erstellen
        if self.kugelnspawn < 10:
            if self.secs == self.spawn:
                self.all_Kugeln.add(Kugeln(self.settings))
                self.kugelnspawn += 1
                self.spawn += 2
        else:
            if self.secs == self.spawn:
                self.spawn += 2

    def faster(self):                                       # Erweiterung der Blasen-Berechnung, schneller jede 15 sek
        pass

if __name__ == '__main__':                                    
    settings = Settings()                               

    pygame.init()                                      

    Spiel = Spiel(pygame, settings)                      

    Spiel.run()                
  
    pygame.quit()