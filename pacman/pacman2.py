import pygame
from abc import ABCMeta, abstractmethod
import random

pygame.init()

screen = pygame.display.set_mode((800, 600), 0)

fonte = pygame.font.SysFont("arial", 24, True, False)
# fonte2 = pygame.font.SysFont("arial", 15, True, False)

AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)
LARANJA = (255, 140, 0)
ROSA = (255, 15, 192)
CIANO = (0, 255, 255)
VELOCIDADE = 1
ACIMA = int(1)
ABAIXO = int(2)
DIREITA = int(3)
ESQUERDA = int(4)

class ElementoJogo(metaclass=ABCMeta):
    @abstractmethod
    def pintar(self, tela):
        pass

    @abstractmethod
    def calcular_regras(self):
        pass

    @abstractmethod
    def processar_eventos(self, eventos):
        pass

class Movivel(metaclass=ABCMeta):
    @abstractmethod
    def aceitar_movimento(self):
        pass
    
    @abstractmethod
    def recusar_movimento(self):
        pass

    @abstractmethod
    def esquina(self, direcoes):
        pass
    
class Cenario(ElementoJogo):
    def __init__(self, tamanho, pac):
        self.pacman = pac
        self.moviveis = []
        self.tamanho = tamanho
        self.estado = 0
        # Estados possíveis 0- Jogando 1- Pausado 2- GameOver 3- Vitoria
        self.pontos = 0
        self.vidas = 5
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def adicionar_movivel(self, obj):
        self.moviveis.append(obj)

    def pintar_score(self, tela): # Cenário: 28 col x 29 lin
        pontos_x = 30 * self.tamanho
        img_pontos = fonte.render("Score: {}".format(self.pontos), True, AMARELO)
        tela.blit(img_pontos, (pontos_x, 50))
        vidas_img = fonte.render("Vidas: {}".format(self.vidas), True, AMARELO)
        tela.blit(vidas_img, (pontos_x, 100))
        
##        linha_img = fonte2.render("Versão Customizada", True, (0, 120, 255))
##        tela.blit(linha_img, (pontos_x, 150))
##        linha_img = fonte2.render("para", True, (0, 120, 255))
##        tela.blit(linha_img, (pontos_x, 170))
##        linha_img = fonte2.render("Guilherme", True, (0, 120, 255))
##        tela.blit(linha_img, (pontos_x, 190))
##        linha_img = fonte2.render("da Silva Vieira", True, (0, 120, 255))
##        tela.blit(linha_img, (pontos_x, 210))
     
  
    def pintar_linha(self, tela, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha):
            x = numero_coluna * self.tamanho
            y = numero_linha * self.tamanho
            half = self.tamanho // 2
            cor = PRETO
            if int(coluna) == 2:
                cor = AZUL
            pygame.draw.rect(tela, cor, (x, y, self.tamanho, self.tamanho), 0)
            if int(coluna) == 1:
                pygame.draw.circle(tela, AMARELO, (x + half, y + half), self.tamanho // 10, 0)

    def pintar_jogando(self, tela):
        for numero_linha, linha in enumerate(self.matriz): # função enumerate devolve o valor e o índice da matriz
            self.pintar_linha(tela, numero_linha, linha)
        self.pintar_score(tela)

    def pintar(self, tela):
        if self.estado == 0:
            self.pintar_jogando(tela)
        elif self.estado == 1:
            self.pintar_jogando(tela)
            self.pintar_pausado(tela)
        elif self.estado == 2:
            self.pintar_jogando(tela)
            self.pintar_gameover(tela)
        elif self.estado == 3:
            self.pintar_jogando(tela)
            self.pintar_vitoria(tela)            

    def pintar_texto_centro(self, tela, texto):
        texto_img = fonte.render(texto, True, AMARELO)
        texto_x = (tela.get_width() - texto_img.get_width()) // 2
        texto_y = (tela.get_height() - texto_img.get_height()) // 2
        tela.blit(texto_img, (texto_x, texto_y))

    def pintar_vitoria(self, tela):
        self.pintar_texto_centro(tela, "W I N N E R  ! ! !")

    def pintar_gameover(self, tela):
        self.pintar_texto_centro(tela, "G A M E  O V E R")       
  
    def pintar_pausado(self, tela):
        self.pintar_texto_centro(tela, "P A U S E")
       
    def get_direcoes(self, linha, coluna):
        direcoes = []
        if self.matriz[int(linha - 1)][int(coluna)] != 2: # acima não e uma parede
            direcoes.append(ACIMA)
        if self.matriz[int(linha + 1)][int(coluna)] != 2: # abaixo não e uma parede
            direcoes.append(ABAIXO)
        if self.matriz[int(linha)][int(coluna + 1)] != 2: # a direita não e uma parede
            direcoes.append(DIREITA)
        if self.matriz[int(linha)][int(coluna - 1)] != 2: # a esquerda não e uma parede
            direcoes.append(ESQUERDA)
        return direcoes            

    def calcular_regras(self):
        if self.estado == 0:
            self.calcular_regras_jogando()
        elif self.estado == 1:
            self.calcular_regras_pausado()
        elif self.estado == 2:
            self.calcular_regras_gameover()

    def calcular_regras_gameover(self):
        pass
     
    def calcular_regras_jogando(self):
        for movivel in self.moviveis:
            lin = int(movivel.linha)
            col = int(movivel.coluna)
            lin_intencao = int(movivel.linha_intencao)
            col_intencao = int(movivel.coluna_intencao)
            direcoes = self.get_direcoes(lin, col)
            if len(direcoes) >= 3:
                movivel.esquina(direcoes)

            if isinstance(movivel, Fantasma) and movivel.linha == self.pacman.linha and\
               movivel.coluna == self.pacman.coluna:
               self.vidas -= 1
               if self.vidas <= 0:
                   self.estado = 2 # game over
               else:
                   self.pacman.linha = 1
                   self.pacman.coluna = 1                   
            else:    
                if 0 <= col_intencao < 28 and 0 <= lin_intencao < 29 and \
                    self.matriz[lin_intencao][col_intencao] != 2:
                    movivel.aceitar_movimento()
                    if isinstance(movivel, Pacman) and self.matriz[lin][col] == 1:
                        self.pontos += 1
                        self.matriz[lin][col] = 0
                        if self.pontos >= 306: # game winner
                            self.estado = 3
                else:
                    movivel.recusar_movimento(direcoes)

    def calcular_regras_pausado(self):
        pass
              
    def processar_eventos(self, evts):
        for e in evts:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    if self.estado == 0:
                        self.estado = 1
                    else:
                        self.estado = 0                  

class Pacman(ElementoJogo, Movivel):
    def __init__(self, size):
        self.coluna = 1
        self.linha = 1
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = size # diametro em pixels, 30 colunas
        self.raio = int(self.tamanho // 2)
        self.vel_x = 0
        self.vel_y = 0
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.abertura = 0
        self.velocidade_abertura = 1 # abertura da boca do Pacman

    def pintar(self, tela):
        # desenhar o corpo do pacman
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio)

        self.abertura += self.velocidade_abertura
        if self.abertura > self.raio:
            self.velocidade_abertura = -1
        if self.abertura <= 0:
            self.velocidade_abertura = 1

        # Desenho da boca do Pacman
        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.raio, self.centro_y - self.abertura)
        labio_inferior = (self.centro_x + self.raio, self.centro_y + self.abertura)
        pontos = [canto_boca, labio_superior, labio_inferior]      
        pygame.draw.polygon(tela, PRETO, pontos, 0)

        # Desenho do olho do Pacman
        olho_x = int(self.centro_x + self.raio / 3)
        olho_y = int(self.centro_y - self.raio * 0.7)
        olho_raio = int(self.raio / 10)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def calcular_regras(self):
        self.coluna_intencao = self.coluna + self.vel_x
        self.linha_intencao  = self.linha + self.vel_y
        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

    def processar_eventos(self, eventos):
         for e in eventos:
           if e.type == pygame.KEYDOWN:
               # print(e.key)
               if e.key == pygame.K_RIGHT: ## seta para direita
                   self.vel_x = VELOCIDADE
               elif e.key == pygame.K_LEFT: ## seta para esquerda
                   self.vel_x = -VELOCIDADE
               elif e.key == pygame.K_UP: ## seta para cima
                   self.vel_y = -VELOCIDADE
               elif e.key == pygame.K_DOWN: ## seta para baixo
                   self.vel_y = VELOCIDADE
           elif e.type == pygame.KEYUP: ## tecla foi liberada
               if e.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                   self.vel_x = 0
               elif e.key in [pygame.K_UP, pygame.K_DOWN]:
                   self.vel_y = 0

    def processar_eventos_mouse(self, eventos):
        delay = 100
        for e in eventos:
            if e.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = e.pos
                self.coluna = (mouse_x - self.centro_x) / delay
                self.linha = (mouse_y - self.centro_y) /delay

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna

    def esquina(self, direcoes):
        pass 
        
##        Desenho em espelho do Pacman 
##        labio_superior = (self.centro_x - self.raio, self.centro_y - self.raio)
##        labio_inferior = (self.centro_x - self.raio, self.centro_y)
##        olho_x = int(self.centro_x - self.raio / 3)
##        olho_y = int(self.centro_y - self.raio * 0.70)
##        canto_boca = (self.centro_x, self.centro_y)
##        pontos = [canto_boca, labio_superior, labio_inferior]     
##        pygame.draw.polygon(tela, PRETO, pontos, 0)
##        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

class Fantasma(ElementoJogo, Movivel):
    def __init__(self, cor, tamanho):
        self.coluna = 13.0
        self.linha = 15.0
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.cor = cor
        self.tamanho = tamanho
        self.direcao = ABAIXO
        self.velocidade = 1
        
    def pintar(self, tela):
        fatia = self.tamanho // 8
        px = int(self.coluna * self.tamanho)
        py = int(self.linha * self.tamanho)
        contorno = [(px, py + self.tamanho),
                    (px + fatia, py + fatia * 2 ),
                    (px + fatia * 2, py + fatia // 2),
                    (px + fatia * 3, py),
                    (px + fatia * 5, py),
                    (px + fatia * 6, py + fatia // 2),
                    (px + fatia * 7, py + fatia * 2),
                    (px + self.tamanho, py + self.tamanho)]
        pygame.draw.polygon(tela, self.cor, contorno, 0)

        olho_raio_ext = fatia
        olho_raio_int = fatia // 2

        olho_e_x = int(px + fatia * 2.5)
        olho_e_y = int(py + fatia * 2.5)

        olho_d_x = int(px + fatia * 5.5)
        olho_d_y = int(py + fatia * 2.5)

        pygame.draw.circle(screen, BRANCO, (olho_e_x, olho_e_y), olho_raio_ext)
        pygame.draw.circle(screen, PRETO, (olho_e_x, olho_e_y), olho_raio_int)
        pygame.draw.circle(screen, BRANCO, (olho_d_x, olho_d_y), olho_raio_ext)
        pygame.draw.circle(screen, PRETO, (olho_d_x, olho_d_y), olho_raio_int)
   
    def calcular_regras(self):
        if self.direcao == ACIMA:
            self.linha_intencao -= self.velocidade
        elif self.direcao == ABAIXO:
            self.linha_intencao += self.velocidade
        elif self.direcao == DIREITA:
            self.coluna_intencao += self.velocidade
        elif self.direcao == ESQUERDA:
            self.coluna_intencao -= self.velocidade

    def mudar_direcao(self, direcoes):
        self.direcao = random.choice(direcoes)

    def esquina(self, direcoes):
        self.mudar_direcao(direcoes)

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcao(direcoes)        

    def processar_eventos(self, evts):
        pass

if __name__ == "__main__":
    size = 600 // 30
    pacman = Pacman(size)
    blinky = Fantasma(VERMELHO, size)
    inky = Fantasma(CIANO, size)
    clyde = Fantasma(LARANJA, size)
    pinky = Fantasma(ROSA, size)
    cenario = Cenario(size, pacman)
    cenario.adicionar_movivel(pacman)
    cenario.adicionar_movivel(blinky)
    cenario.adicionar_movivel(inky)
    cenario.adicionar_movivel(clyde)
    cenario.adicionar_movivel(pinky)
    
    while True:
        
        #Calcular as regras
        pacman.calcular_regras()
        blinky.calcular_regras()
        inky.calcular_regras()
        clyde.calcular_regras()
        pinky.calcular_regras()
        cenario.calcular_regras()
        
        #Pintar a tela
        screen.fill(PRETO)

        cenario.pintar(screen)
        pacman.pintar(screen)
        blinky.pintar(screen)
        inky.pintar(screen)
        clyde.pintar(screen)
        pinky.pintar(screen)
        
        pygame.display.update()
        pygame.time.delay(50) # 100

        #Captura os eventos
        eventos = pygame.event.get()
        pacman.processar_eventos(eventos)
        cenario.processar_eventos(eventos)
##        for e in eventos:
##            if e.type == pygame.QUIT:
##                exit()
        # pacman.processar_eventos_mouse(eventos)
        #pacman.processar_eventos(eventos)
       
            
        







        
