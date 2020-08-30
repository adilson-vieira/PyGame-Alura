import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600), 0)

pontos = 10
texto = "Score{}: ".format(pontos)

fonte = pygame.font.SysFont("arial", 48, True, False) # tipo, tamanho, negrito, itálico
imagem_texto = fonte.render(texto, True, (255, 255, 0)) # transforma em uam surface texto, antialiase, cor

while True:

    screen.blit(imagem_texto, (100, 100) )
    pygame.display.update()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
