import pygame
from .settings import *
from .gerador import check_sum

class Block(pygame.sprite.Sprite):
    def __init__(self, index):
        super().__init__()
        self.colors = ['Blue', 'Green', 'Red']
        self.index=index
        self.number=None
        self.in_sum = None
        self.time_clicked = None

    def setNumber(self, numbers):

        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        self.image.fill(self.colors[self.index])
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH/2, SCREEN_HEIGHT-FLOOR_HEIGHT-self.index*SQUARE_SIZE)

        self.in_sum = check_sum(self.index, numbers)
        self.number = numbers[self.index]

        self.fonte = pygame.font.Font(None, int(SCREEN_WIDTH/16))
        self.texto_renderizado = self.fonte.render(str(self.number), True, (0, 0, 0))  
        self.texto_rect = self.texto_renderizado.get_rect(center=(SQUARE_SIZE // 2, SQUARE_SIZE // 2))
        self.image.blit(self.texto_renderizado, self.texto_rect)

    def checkClick(self, points, lifes):
        self.time_clicked=pygame.time.get_ticks()
        self.image.fill((0,0,0,0))
        self.fonte = pygame.font.Font(None, 30)
        if self.in_sum:
            self.texto_renderizado = self.fonte.render("RIGHT", True, (0, 255, 0))  
            self.texto_rect = self.texto_renderizado.get_rect(center=(SQUARE_SIZE // 2, SQUARE_SIZE // 2))
            self.image.blit(self.texto_renderizado, self.texto_rect)
            return (points + 1, lifes)
        else:
            self.texto_renderizado = self.fonte.render("WRONG", True, (255, 0, 0))  
            self.texto_rect = self.texto_renderizado.get_rect(center=(SQUARE_SIZE // 2, SQUARE_SIZE // 2))
            self.image.blit(self.texto_renderizado, self.texto_rect)
            return (points, lifes - 1)
""" 
    def update(self):
        if self.time_clicked != None:
            if pygame.time.get_ticks() - self.time_clicked > 1000:
                self.time_clicked=None
                reset=True
                return reset """