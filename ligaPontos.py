########################################################
### Gera uma malha (matriz) com N linhas e M colunas ###
### sorteia dois pontos diversos entre sí e os liga  ###
### com o caminho mais curto.                        ###
########################################################
### Prof. Filipo Mor                                 ###
########################################################

import random

N = 20 # quantidade de linhas
M = 20 # quantidade de colunas

###
### Mostra a malha no console, incluindo identificadores
### de linah e coluna
###
def MostraMatriz(titulo, matriz):
    print(f"\n{titulo}")
    print("  ", end="")
    [print(f" {i:2d}", end="") for i in range(M)]
    print("\n", end="")
    for i in range(N):
        print(i, end=" ")
        for j in range(M):
            print(f" {matriz[i][j]} ", end="" )
        print("\n", end="")

###
### Cria a matriz e a popula com o caracter indicado
###
def PopulaMatriz(qtLinhas, qtColunas, caracter):
    matriz = [[caracter] * qtColunas for i in range(qtLinhas)] # cria a matriz populada com o caracter informado
    for i in range(qtLinhas): # preenche a matriz com o caracter informado
        for j in range(qtColunas):
            matriz[i][j] = caracter
    return matriz


# sorteia dois pontos dentro da matriz
pontoO = (Ax, Ay) = (random.randint(0, N - 1), random.randint(0, M - 1))
pontoD = (Bx, By) = (random.randint(0, N - 1), random.randint(0, M - 1))

'''
# garante que os pontos sejam diversos
while pontoO == pontoD:
    pontoD = (random.randint(0, N - 1), random.randint(0, M - 1))
'''

# garante que pontoO esteja a esquerda e acima do pontoD
while (pontoO[0] > pontoD[0] or pontoO[1] > pontoD[1]) or (pontoO == pontoD):
    pontoO = (random.randint(0, N - 1), random.randint(0, M - 1))


###
### mostra a malha com os pontos selecionados
###
matriz = PopulaMatriz(N, M, '.')
matriz[pontoO[0]][pontoO[1]] = 'O' # ponto de Origem
matriz[pontoD[0]][pontoD[1]] = 'X' # ponto de Destino
MostraMatriz("Matriz Original", matriz)

# calcula distancia entre os pontos
distancia = abs(pontoO[0] - pontoD[0]) + abs(pontoO[1] - pontoD[1])
distX = abs(pontoO[0] - pontoD[0]) / distancia
distY = abs(pontoO[1] - pontoD[1]) / distancia
pontoIntermediario = pontoO
# depuracao
print(f"\nPonto O: {pontoO}")
print(f"Ponto D: {pontoD}")
print(f"\nDistancia entre os pontos: {distancia}")
print(f"Distancia X: {distX}")
print(f"Distancia Y: {distY}")

###
### percorre o caminho entre os pontos, preenchendo-o com '*'
###
for i in range(distancia):
    pontoIntermediario = (pontoIntermediario[0] + distX, pontoIntermediario[1] + distY)
    print(f"Ponto Intermediario: {pontoIntermediario}") # depuracao
    matriz[int(pontoIntermediario[0])][int(pontoIntermediario[1])] = '*'

# mostra a malha com o caminho marcado
matriz[pontoO[0]][pontoO[1]] = 'O'
matriz[pontoD[0]][pontoD[1]] = 'X'
MostraMatriz("Pontos ligados", matriz)