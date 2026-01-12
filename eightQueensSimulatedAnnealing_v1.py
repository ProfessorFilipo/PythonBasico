import random
import math
import pygame
import sys

# Configurações
TAM_CELULA = 60
NUM_RAINHAS = 8
LARGURA = TAM_CELULA * NUM_RAINHAS
ALTURA = TAM_CELULA * NUM_RAINHAS + 50  # espaço para o botão

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("8 Rainhas com Simulated Annealing")

font = pygame.font.SysFont(None, 36)

def numero_deconflitos(solu):
    """Calcula o número de pares de rainhas em conflito."""
    conflitos = 0
    for i in range(NUM_RAINHAS):
        for j in range(i + 1, NUM_RAINHAS):
            if abs(i - j) == abs(solu[i] - solu[j]):
                conflitos += 1
    return conflitos

def gerar_proxima_configuracao(solu):
    """Gera uma nova configuração movendo uma rainha aleatoriamente."""
    nova_solu = solu[:]
    col = random.randint(0, NUM_RAINHAS - 1)
    nova_linha = random.randint(0, NUM_RAINHAS - 1)
    nova_solu[col] = nova_linha
    return nova_solu

def simulated_annealing():
    """Executa o algoritmo de simulated annealing para encontrar solução para as 8 rainhas."""
    # solução inicial aleatória
    solu = [random.randint(0, NUM_RAINHAS - 1) for _ in range(NUM_RAINHAS)]
    temperatura = 100.0
    taxa_resfriamento = 0.99
    min_temperatura = 0.1
    max_iter = 10000

    for _ in range(max_iter):
        conflitos_atual = numero_deconflitos(solu)
        if conflitos_atual == 0:
            return solu
        nova_solu = gerar_proxima_configuracao(solu)
        conflitos_nova = numero_deconflitos(nova_solu)
        delta = conflitos_nova - conflitos_atual

        if delta < 0:
            solu = nova_solu
        else:
            prob = math.exp(-delta / temperatura)
            if random.random() < prob:
                solu = nova_solu

        temperatura *= taxa_resfriamento
        if temperatura < min_temperatura:
            break
    return solu

def desenhar_tabuleiro():
    for linha in range(NUM_RAINHAS):
        for coluna in range(NUM_RAINHAS):
            cor = BRANCO if (linha + coluna) % 2 == 0 else PRETO
            rect = pygame.Rect(coluna * TAM_CELULA, linha * TAM_CELULA, TAM_CELULA, TAM_CELULA)
            pygame.draw.rect(screen, cor, rect)

def desenhar_rainhas(solu):
    for coluna, linha in enumerate(solu):
        center_x = coluna * TAM_CELULA + TAM_CELULA // 2
        center_y = linha * TAM_CELULA + TAM_CELULA // 2
        radius = TAM_CELULA // 3
        pygame.draw.circle(screen, VERMELHO, (center_x, center_y), radius)

def desenhar_botao():
    rect = pygame.Rect(10, ALTURA - 50, 250, 40)
    pygame.draw.rect(screen, AZUL, rect)
    texto = font.render("Gerar Nova Solução", True, BRANCO)
    texto_rect = texto.get_rect(center=rect.center)
    screen.blit(texto, texto_rect)
    return rect

def main():
    # Gera a primeira solução ao iniciar
    solu = simulated_annealing()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                botao_rect = pygame.Rect(10, ALTURA - 50, 250, 40)
                if botao_rect.collidepoint(mouse_pos):
                    # Gera uma nova solução ao clicar no botão
                    solu = simulated_annealing()

        desenhar_tabuleiro()
        desenhar_rainhas(solu)
        desenhar_botao()
        pygame.display.flip()
        clock.tick(60)