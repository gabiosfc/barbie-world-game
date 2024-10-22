import matplotlib.pyplot as plt
import random
import heapq
import math

barbie = (23, 19)
amigos = [
    (5, 13), # amigo 1
    (10, 9), # amigo 2
    (36, 15), # amigo 3
    (6, 35), # amigo 4
    (24, 38), # amigo 5
    (37, 37) # amigo 6
]

# Função para atribuir a cor conforme o valor da célula
def obter_cor(valor):
    if valor == 0:
        return 'orange'  # Laranja - Células proibidas
    elif valor == 1:
        return 'gray'    # Cinza
    elif valor == 3:
        return 'brown'   # Marrom
    elif valor == 5:
        return 'green'   # Verde
    elif valor == 10:
        return 'white'   # Branca
    elif valor == 100:
        return 'pink'   # Rosa - Percurso
    else:
        return 'black'   # Valor inesperado (preto)

# Função para carregar a matriz do arquivo TXT
def carregar_matriz(arquivo_txt):
    with open(arquivo_txt, 'r') as arquivo:
        # Ler cada linha do arquivo e converter em uma lista de listas de inteiros
        return [list(map(int, linha.strip().split(','))) for linha in arquivo]

# Função para exibir o mapa
def exibir_mapa(mapa):
    # Configurar a figura e os eixos
    fig, ax = plt.subplots()

    # Exibir a matriz com as cores correspondentes
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            valor = mapa[i][j]
            cor = obter_cor(valor)
            rect = plt.Rectangle([j, len(mapa) - i - 1], 1, 1, facecolor=cor)
            ax.add_patch(rect)

    # Exibir o mapa
    plt.xlim(0, len(mapa[0]))
    plt.ylim(0, len(mapa))
    plt.gca().set_aspect('equal', adjustable='box')  # Manter a proporção
    plt.axis('off')  # Remover os eixos
    plt.show()

# Coordenadas de posições da Barbie e amigos
def definir_posicao_personagens(mapa):
    mapa [barbie[0]][barbie[1]] = 99
    for a, b in amigos:
        mapa [a][b] = 99
    return mapa

# Exibição do percurso realizado pela Barbie
def exibir_percurso(mapa, percurso):
    for x, y in percurso:
        casa_atual = mapa[x][y]
        mapa [x][y] = 100
        exibir_mapa(mapa) # inserir delay
        mapa [x][y] = casa_atual
    return mapa

# Sorteio amigos que responderão SIM
def sortear_amigos(qtd):
    return random.sample(amigos, qtd)  # Sorteia diretamente os amigos
# Sortear 3 amigos
resultado = sortear_amigos(3)
print(resultado)


# Cálculo da heurística utilizando distância Manhattan
def calcular_heuristica(ponto_atual, ponto_destino):
    return abs(ponto_atual[0] - ponto_destino[0]) + abs(ponto_atual[1] - ponto_destino[1])

def calcular_custo_movimento(terreno):
    custos = {
        1: 1,  # Asfalto
        3: 3,  # Terra
        5: 5,  # Grama
        10: 10,  # Paralelepípedo
        0: float('inf')  # Edifício (intransponível)
    }
    return custos[terreno]

# Algoritmo A* levando em conta os diferentes terrenos
def a_star(mapa, inicio, destino):
    filas_prioridade = []
    heapq.heappush(filas_prioridade, (0, inicio))
    custo_acumulado = {inicio: 0}
    caminho = {inicio: None}

    while filas_prioridade:
        _, ponto_atual = heapq.heappop(filas_prioridade)

        if ponto_atual == destino:
            caminho_final = []
            while ponto_atual:
                caminho_final.append(ponto_atual)
                ponto_atual = caminho[ponto_atual]
            return caminho_final[::-1]

        vizinhos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for movimento in vizinhos:
            vizinho = (ponto_atual[0] + movimento[0], ponto_atual[1] + movimento[1])

            if 0 <= vizinho[0] < len(mapa) and 0 <= vizinho[1] < len(mapa[0]):
                terreno = mapa[vizinho[0]][vizinho[1]]
                novo_custo = custo_acumulado[ponto_atual] + calcular_custo_movimento(terreno)

                if vizinho not in custo_acumulado or novo_custo < custo_acumulado[vizinho]:
                    custo_acumulado[vizinho] = novo_custo
                    prioridade = novo_custo + calcular_heuristica(vizinho, destino)
                    heapq.heappush(filas_prioridade, (prioridade, vizinho))
                    caminho[vizinho] = ponto_atual

    return None














# percurso = [(23, 20),(23, 21), (22, 21), (21, 21), (20, 21)]

# Arquivo do qual a matriz será carregada
arquivo_txt = 'mapa.txt'

# Carregar a matriz e exibir o mapa
mapa = carregar_matriz(arquivo_txt)
mapa = definir_posicao_personagens(mapa)
# mapa = exibir_percurso (mapa, percurso)
exibir_mapa(mapa)
