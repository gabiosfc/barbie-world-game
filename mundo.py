import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
from heapq import heappop, heappush
from itertools import permutations
import random
import time

# Função para atribuir a cor conforme o valor da célula
def obter_cor(valor, posicao, amigos):
    if valor == -1:
        return 'orange'  # Laranja - Células proibidas
    elif posicao in amigos:
        return 'violet'   # Lilás - Localizações dos amigos
    elif valor == 1:
        return 'gray'    # Cinza
    elif valor == 3: # Terra
        return 'brown'   # Marrom
    elif valor == 5: # Grama
        return 'green'   # Verde
    elif valor == 10: # Paralelepípedo
        return 'white'   # Branca
    else:
        return 'black'   # Valor inesperado (preto)

# Carregar a matriz do arquivo CSV
arquivo_csv = 'mapa.csv'
with open(arquivo_csv, 'r') as arquivo:
    leitor_csv = csv.reader(arquivo)
    mapa = [list(map(int, linha)) for linha in leitor_csv]

# Função para calcular a distância euclidiana entre dois pontos
def distancia_euclidiana(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Função para calcular o custo do movimento com base no valor da célula
def custo_terreno(valor):
    if valor == 1:   # Asfalto
        return 1
    elif valor == 3: # Terra
        return 3
    elif valor == 5: # Grama
        return 5
    elif valor == 10: # Paralelepípedo
        return 10
    return float('inf') # Custo infinito para células inválidas

# Função A* para encontrar o caminho
def a_star(mapa, start, goal):
    num_linhas = len(mapa)
    num_colunas = len(mapa[0])
    
    # Movimentos possíveis (esquerda, direita, cima, baixo)
    movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Heap para manter os nós da open list
    open_list = []
    heappush(open_list, (0, start))
    
    # Dicionários para armazenar o custo total (g) e o caminho
    g_score = {start: 0}
    came_from = {}
    
    while open_list:
        # Pegar o nó com menor f
        _, current = heappop(open_list)
        
        # Verificar se chegamos ao destino
        if current == goal:
            caminho = []
            while current in came_from:
                caminho.append(current)
                current = came_from[current]
            caminho.append(start)
            caminho.reverse()
            return caminho, g_score[goal]
        
        # Verificar os vizinhos
        for movimento in movimentos:
            neighbor = (current[0] + movimento[0], current[1] + movimento[1])
            
            # Verificar se o vizinho está dentro dos limites do mapa
            if 0 <= neighbor[0] < num_linhas and 0 <= neighbor[1] < num_colunas:
                # Ignorar células proibidas
                if mapa[neighbor[0]][neighbor[1]] == -1:
                    continue
                
                # Calcular o custo do movimento para o vizinho
                tentative_g_score = g_score[current] + custo_terreno(mapa[neighbor[0]][neighbor[1]])
                
                # Verificar se encontramos um caminho melhor
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    # Cálculo da heurística (distância euclidiana até o objetivo)
                    h_score = distancia_euclidiana(neighbor, goal)
                    f_score = tentative_g_score + h_score  # f = g + h
                    heappush(open_list, (f_score, neighbor))
    
    return None, float('inf')  # Se não houver caminho

# Função para realizar o sorteio de 3 amigos que dirão SIM
def sorteio_amigos(amigos):
    return random.sample(amigos, 3)

# Função para calcular o custo heurístico e buscar amigos
def calcular_melhor_percurso(barbie, amigos):
    todas_permutacoes = permutations(amigos)
    
    menor_distancia = float('inf')
    melhor_percurso = None

    # Verificar cada permutação para encontrar a menor distância total
    for permutacao in todas_permutacoes:
        distancia_total = 0
        caminho_total = []
        
        # Distância da Barbie até o primeiro amigo
        caminho, dist = a_star(mapa, barbie, tuple(permutacao[0]))
        if caminho is None:
            continue
        distancia_total += dist
        caminho_total += caminho
        
        # Somar as distâncias entre os amigos
        for i in range(len(permutacao) - 1):
            caminho, dist = a_star(mapa, tuple(permutacao[i]), tuple(permutacao[i + 1]))
            if caminho is None:
                continue
            distancia_total += dist
            caminho_total += caminho
        
        # Distância do último amigo de volta para o ponto inicial (Barbie)
        caminho, dist = a_star(mapa, tuple(permutacao[-1]), barbie)
        if caminho is None:
            continue
        distancia_total += dist
        caminho_total += caminho

        # Atualizar a menor distância e o melhor percurso
        if distancia_total < menor_distancia:
            menor_distancia = distancia_total
            melhor_percurso = caminho_total

    return menor_distancia, melhor_percurso

# Coordenadas dos pontos
barbie = (23, 19)
amigos = [
    (5, 13), # amigo 1
    (10, 9), # amigo 2
    (36, 15), # amigo 3
    (6, 35), # amigo 4
    (24, 38), # amigo 5
    (37, 37) # amigo 6
]

# Sorteio de 3 amigos que responderão SIM
amigos_sim = sorteio_amigos(amigos)

# Exibir os amigos sorteados
print("Amigos que responderão SIM:")
for amigo in amigos_sim:
    print(f"Amigo em {amigo}")

# Medir o tempo de execução
inicio_execucao = time.time()

# Calcular o melhor percurso
menor_distancia, melhor_percurso = calcular_melhor_percurso(barbie, amigos)

# Exibir o resultado
fim_execucao = time.time()
tempo_execucao = fim_execucao - inicio_execucao
print("Menor distância possível:", menor_distancia)
print("Melhor percurso:", melhor_percurso)
print(f"Tempo de execução: {tempo_execucao:.4f} segundos")

# Exibir o percurso no mapa
fig, ax = plt.subplots()
ax.set_xticks([])
ax.set_yticks([])

# Exibir a matriz com as cores correspondentes
for i in range(len(mapa)):
    for j in range(len(mapa[0])):
        valor = mapa[i][j]
        cor = obter_cor(valor, (i, j), amigos_sim)  # Adicionando a posição atual
        rect = plt.Rectangle([j, len(mapa) - i - 1], 1, 1, facecolor=cor)
        ax.add_patch(rect)

# Desenhar o caminho encontrado
if melhor_percurso:
    for step in melhor_percurso:
        rect = plt.Rectangle([step[1], len(mapa) - step[0] - 1], 1, 1, facecolor='red')
        ax.add_patch(rect)

# Exibir o gráfico
plt.xlim(0, len(mapa[0]))
plt.ylim(0, len(mapa))
plt.gca().set_aspect('equal', adjustable='box')  # Manter a proporção
plt.show()
