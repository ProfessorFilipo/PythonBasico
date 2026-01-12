import numpy as np
import random

N = 3

def PopulaMatriz(qtLinhas, qtColunas, menorValor, maiorValor):
    matriz = [[0] * qtColunas for i in range(qtLinhas)] # cria a matriz populada com zeros
    for i in range(qtLinhas): # preenche a matriz com inteiros aleatorios
        for j in range(qtColunas):
            matriz[i][j] = random.randint(menorValor, maiorValor)
    return matriz

def MostraMatriz(matriz, titulo):
    print("\n" + titulo)
    for L in range(len(matriz)):
        for C in range(len(matriz[L])):
            print(f"  {int(matriz[L][C]):2d} ", end="")
        print()

def fatoraLU(matriz):
    U = np.copy(matriz)
    linhas = np.shape(U)[0]
    L = np.eye(linhas)
    for j in np.arange(linhas-1):
        for i in np.arange(j+1, linhas):
            L[i][j] = U[j][i] / U[j][j]
            for k in np.arange(j+1, linhas):
                U[i][k] = U[i][k] - L[i][k] * U[j][k]
            U[i][j] = 0
    return L, U

#Ma = [[1, 1, 1], [4, 3, -1], [3, 5, 3]]
Ma = PopulaMatriz(N, N, 1, 9)
MostraMatriz(Ma, "Matriz A")

# popula a matriz com valores 1
Mb = np.ones([N, N])
MostraMatriz(Mb, 'Matriz B')

Mi = np.eye(N)
MostraMatriz(Mi, 'Matriz identidade')

MaT = np.transpose(Mb)
MostraMatriz(MaT, 'Matriz Transposta de B')


Ml, Mu = fatoraLU(Ma)
MostraMatriz(Ml, 'Matriz L')
MostraMatriz(Mu, 'Matriz U')



