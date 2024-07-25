import pygame
from gerador import gera_numeros, check_sum
from sys import exit

pygame.init()
pygame.display.set_caption("TESTE")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FLOOR_HEIGHT = 50
SQUARE_SIZE = 100

PLAY_TIME_SECONDS = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

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

        self.fonte = pygame.font.Font(None, 50)
        self.texto_renderizado = self.fonte.render(str(self.number), True, (0, 0, 0))  
        self.texto_rect = self.texto_renderizado.get_rect(center=(SQUARE_SIZE // 2, SQUARE_SIZE // 2))
        self.image.blit(self.texto_renderizado, self.texto_rect)

    def checkClick(self):
        global points
        self.time_clicked=pygame.time.get_ticks()
        self.image.fill((0,0,0,0))
        self.fonte = pygame.font.Font(None, 30)
        if self.in_sum:
            points+=1
            self.texto_renderizado = self.fonte.render("RIGHT", True, (0, 255, 0))  
            self.texto_rect = self.texto_renderizado.get_rect(center=(SQUARE_SIZE // 2, SQUARE_SIZE // 2))
            self.image.blit(self.texto_renderizado, self.texto_rect)
        else:
            self.texto_renderizado = self.fonte.render("WRONG", True, (255, 0, 0))  
            self.texto_rect = self.texto_renderizado.get_rect(center=(SQUARE_SIZE // 2, SQUARE_SIZE // 2))
            self.image.blit(self.texto_renderizado, self.texto_rect)

    def update(self):
        global reset
        if self.time_clicked != None:
            if pygame.time.get_ticks() - self.time_clicked > 1000:
                reset=True
                self.time_clicked=None


block_group = pygame.sprite.Group()
blocks = [Block(0), Block(1), Block(2)]
for b in blocks:
    block_group.add(b)

reset=True
points = 0
game_mode = 'menu'
started_time = None

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and game_mode=='running':
            mouse_pos = event.pos 
            for b in block_group:
                if b.rect.collidepoint(mouse_pos):
                    b.checkClick()
                    print(f"Block clicked! {b.number}")

    match game_mode:

        case 'menu':
            screen.fill((255,255,255))

            font = pygame.font.Font(None, 60)
            play_text = font.render("PLAY", True, 'Black')
            play_text_rect = play_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(play_text,play_text_rect)

            mouse_pos = pygame.mouse.get_pos()
            clicked = pygame.mouse.get_pressed()[0]
            if play_text_rect.collidepoint(mouse_pos) and clicked:
                game_mode = 'running'
                started_time = pygame.time.get_ticks()
                points = 0

        case 'running':

            left_time = int((pygame.time.get_ticks() - started_time)/1000)

            screen.fill((255,255,255))
            pygame.draw.rect(screen, (200,200,200), (0,SCREEN_HEIGHT-FLOOR_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT))

            if reset:
                numbers = gera_numeros()
                for i in range(3):
                    blocks[i].setNumber(numbers)
                reset = not(reset)

            block_group.update()
            block_group.draw(screen)

            font = pygame.font.Font(None, 50)
            gameover_text = font.render(f"Sum: {str(numbers[3])}", True, 'Black')
            gameover_text_rect = gameover_text.get_rect(topleft=(10, 10))
            screen.blit(gameover_text,gameover_text_rect)

            time_text = font.render(f"{PLAY_TIME_SECONDS - left_time}", True, 'Black')
            time_text_rect = time_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
            screen.blit(time_text,time_text_rect)

            if PLAY_TIME_SECONDS - left_time <= 0:
                game_mode = 'gameover' 

        case 'gameover':
            print(points)
            screen.fill((0,0,0))
            font = pygame.font.Font(None, 60)

            gameover_text = font.render(f"GAME OVER", True, 'White')
            gameover_text_rect = gameover_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
            screen.blit(gameover_text,gameover_text_rect)

            score_text = font.render(f"score: {points}", True, 'White')
            score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(score_text,score_text_rect)

            restart_text = font.render(f"RESTART", True, 'White')
            restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 100))
            screen.blit(restart_text,restart_text_rect)

            mouse_pos = pygame.mouse.get_pos()
            clicked = pygame.mouse.get_pressed()[0]
            if restart_text_rect.collidepoint(mouse_pos) and clicked:
                game_mode = 'running'
                points = 0
                started_time = pygame.time.get_ticks()

    pygame.display.update()
    clock.tick(60)      