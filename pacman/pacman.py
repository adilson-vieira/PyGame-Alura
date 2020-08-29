import pygame

AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
VELOCIDADE = 1
RAIO = 30

pygame.init()

tela = pygame.display.set_mode((640, 480))
x = 10
y = 10
vel_x = VELOCIDADE
vel_y = VELOCIDADE

while True:

        # Calcula as regras
        x += vel_x
        y += vel_y

        if x > 640 - RAIO:
            vel_x = -VELOCIDADE
        elif x < RAIO:
            vel_x = VELOCIDADE

        if y > 480 - RAIO:
            vel_y = -VELOCIDADE
        elif y < RAIO:
            vel_y = VELOCIDADE

        # Pinta
        tela.fill(PRETO)
        pygame.draw.circle(tela, AMARELO, (int(x), int(y)), RAIO, 0)
        pygame.display.update()

        # Eventos
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
