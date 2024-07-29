import pygame
from project.settings import *
from project.gerador import gera_numeros
from project.sprites import *
from sys import exit

pygame.init()
pygame.display.set_caption("TESTE")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

block_group = pygame.sprite.Group()
for i in range(3):
    block_group.add(Block(i))

points = 0
lifes = 3
started_time = None
reset = True
game_mode = 'menu'
clicked_time = None

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and game_mode=='running':
            mouse_pos = event.pos 
            for b in block_group:
                if b.rect.collidepoint(mouse_pos):
                    points, lifes = b.checkClick(points, lifes)
                    clicked_time = pygame.time.get_ticks()
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
                lifes = 3
                clicked_time = None
                reset = True

        case 'running':

            left_time = int((pygame.time.get_ticks() - started_time)/1000)

            screen.fill((255,255,255))
            pygame.draw.rect(screen, (200,200,200), (0,SCREEN_HEIGHT-FLOOR_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT))

            if reset:
                numbers = gera_numeros(NUMBERS_RANGE)
                for b in block_group:
                    b.setNumber(numbers)
                reset = False
            else:
                if clicked_time != None and (pygame.time.get_ticks() - clicked_time) > 1000:
                    reset = True
                    clicked_time = None

            block_group.update()
            block_group.draw(screen)

            font = pygame.font.Font(None, 50)

            gameover_text = font.render(f"Sum: {str(numbers[3])}", True, 'Black')
            gameover_text_rect = gameover_text.get_rect(topleft=(10, 10))
            screen.blit(gameover_text,gameover_text_rect)

            lifes_text = font.render(f"Lifes: {lifes}", True, 'Black')
            lifes_text_rect = lifes_text.get_rect(midtop=(SCREEN_WIDTH/2, 10))
            screen.blit(lifes_text,lifes_text_rect)

            time_text = font.render(f"Time: {PLAY_TIME_SECONDS - left_time}", True, 'Black')
            time_text_rect = time_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
            screen.blit(time_text,time_text_rect)

            if PLAY_TIME_SECONDS - left_time <= 0 or lifes <= 0:
                game_mode = 'gameover' 

        case 'gameover':
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
                started_time = pygame.time.get_ticks()
                points = 0
                lifes = 3
                clicked_time = None
                reset = True

    pygame.display.update()
    clock.tick(60)      