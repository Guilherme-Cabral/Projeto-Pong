import random
import sys
import pygame


def bola_centro():
    global velo_bola_x, velo_bola_y
    bola.center = (largura_Tela / 2, comprimento_tela / 2)
    velo_bola_y *= random.choice((1, -1))
    velo_bola_x *= random.choice((1, -1))


def ia_inimiga():
    if inimigo.top < bola.y:
        inimigo.top += velo_inimiga
    if inimigo.bottom > bola.y:
        inimigo.bottom -= velo_inimiga

    if inimigo.bottom >= comprimento_tela:
        inimigo.bottom = comprimento_tela


def animacao_player():
    player.y += velo_player
    if player.top <= 0:
        player.top = 0

    if player.bottom >= comprimento_tela:
        player.bottom = comprimento_tela


def animacao_bola():
    global velo_bola_y, velo_bola_x, Score_oponente, Score_player

    bola.x += velo_bola_x
    bola.y += velo_bola_y

    if bola.top <= 0 or bola.bottom >= comprimento_tela:
        velo_bola_y *= -1

    if bola.left <= 0:
        velo_bola_x *= -1
        Score_oponente += 1
        som_ponto.play()
        bola_centro()

    if bola.right >= largura_Tela:
        velo_bola_x *= -1
        Score_player += 1
        som_ponto.play()
        bola_centro()

    if bola.colliderect(player) or bola.colliderect(inimigo):
        velo_bola_x *= -1
        efeito_sonoro.play()


# configurações de jogo
pygame.init()
pygame.display.set_caption('Pong em Python Made by Guilherme')
tick = pygame.time.Clock()
efeito_sonoro = pygame.mixer.Sound('data/pong.wav')
som_ponto = pygame.mixer.Sound('data/score.wav')

# tela Principal
largura_Tela = 800
comprimento_tela = 600
tela = pygame.display.set_mode((largura_Tela, comprimento_tela))

# entidades
bola = pygame.Rect(largura_Tela / 2 - 15 , comprimento_tela / 2 - 15, 20, 20)
player = pygame.Rect(10, largura_Tela / 2 - 70, 10, 140)
inimigo = pygame.Rect(largura_Tela - 20, comprimento_tela / 2 - 15, 10, 140)

# Cores
preto = (0, 0, 0)
branco = (255, 255, 255)

# Placar
Score_player = 0
Score_oponente = 0
fonte = pygame.font.SysFont('impact', 30)

# Variaveis durr
velo_bola_x = 7 * random.choice((1, -1))
velo_bola_y = 7 * random.choice((1, -1))
velo_player = 0
velo_inimiga = 7


# game logics
while True:

    # inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                velo_player += 7
            if event.key == pygame.K_UP:
                velo_player -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                velo_player -= 7
            if event.key == pygame.K_UP:
                velo_player += 7

    animacao_bola()

    animacao_player()

    ia_inimiga()

    # Desenhando na Janela
    tela.fill(preto)
    pygame.draw.rect(tela, branco, player)
    pygame.draw.rect(tela, branco, inimigo)
    pygame.draw.ellipse(tela, branco, bola)
    pygame.draw.aaline(tela, branco, (largura_Tela / 2, 0), (largura_Tela / 2, comprimento_tela))

    player_text = fonte.render(f'{Score_player}', False, branco)
    tela.blit(player_text, (largura_Tela / 4 - 25, 0))

    opponent_text = fonte.render(f'{Score_oponente}', False, branco)
    tela.blit(opponent_text, (largura_Tela / 2 + 45 * 4, 0))

    pygame.display.update()
    tick.tick(60)
