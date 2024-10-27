import heapq
import random
import time
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

terreno_custo = {5: 5, 1: 1, 3: 3, 10: 10, 0: float("inf")}

class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, node):
        heapq.heappush(self.heap, (node.f, node))

    def extract_min(self):
        return heapq.heappop(self.heap)[1]

    def size(self):
        return len(self.heap)

class Node:
    def __init__(self, x, y, cost, parent=None):
        self.x = x
        self.y = y
        self.cost = cost
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

class AmigosAceitos:
    def __init__(self):
        self.amigos_aceitos = []

    def sortear(self, amigos):
        if not self.amigos_aceitos:
            self.amigos_aceitos = random.sample(amigos, 3)
        return self.amigos_aceitos

    def definir(self, manual_amigos):
        self.amigos_aceitos = manual_amigos
        return self.amigos_aceitos

def carregar_arquivo(file):
    with open(file, "r") as f:
        data = f.read().strip().split("\n")
        return [list(map(int, line.strip().split(','))) for line in data]

def calcular_heuristica(ponto_atual, destinos, heuristicas):
    if ponto_atual not in heuristicas:
        heuristicas[ponto_atual] = min(abs(ponto_atual[0] - destino.x) + abs(ponto_atual[1] - destino.y) for destino in destinos)
    return heuristicas[ponto_atual]

def calcular_astar(start, destinos, grid):
    open_list = MinHeap()
    closed_set = set()
    heuristicas = {}
    destino_coords = [(destino.x, destino.y) for destino in destinos]

    start.g = 0
    start.h = calcular_heuristica((start.x, start.y), destinos, heuristicas)
    start.f = start.g + start.h
    open_list.insert(start)

    start_time_astar = time.time()
    while open_list.size() > 0:
        current_node = open_list.extract_min()
        if (current_node.x, current_node.y) in destino_coords:
            end_time_astar = time.time()
            tempo_execucao_astar = end_time_astar - start_time_astar

            path = []
            temp = current_node
            while temp:
                path.append((temp.x, temp.y))
                temp = temp.parent
            return path[::-1], tempo_execucao_astar
        closed_set.add((current_node.x, current_node.y))
        vizinhos = [
            (current_node.x + 1, current_node.y),
            (current_node.x - 1, current_node.y),
            (current_node.x, current_node.y + 1),
            (current_node.x, current_node.y - 1)
        ]
        for nx, ny in vizinhos:
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                vizinho = Node(nx, ny, grid[ny][nx])
                if terreno_custo[vizinho.cost] == float("inf") or (vizinho.x, vizinho.y) in closed_set:
                    continue
                tentative_g = current_node.g + terreno_custo[vizinho.cost]
                if tentative_g < vizinho.g or (vizinho.x, vizinho.y) not in {n[1] for n in open_list.heap}:
                    vizinho.g = tentative_g
                    vizinho.h = calcular_heuristica((vizinho.x, vizinho.y), destinos, heuristicas)
                    vizinho.f = vizinho.g + vizinho.h
                    vizinho.parent = current_node
                    open_list.insert(vizinho)
    return [], 0

def encontrar_caminho(no_inicial, destinos, grid):
    return calcular_astar(no_inicial, destinos, grid)

def visitar_amigos(no_inicial, amigos_aceitos, grid):
    path_total = []
    amigos_nao_visitados = amigos.copy()
    tempo_total_execucao_astar = 0  # Variável para armazenar o tempo total de execução do A*
    while amigos_nao_visitados:
        destinos = [Node(amigo[0], amigo[1], grid[amigo[1]][amigo[0]]) for amigo in amigos_nao_visitados]
        path, tempo_execucao_astar = encontrar_caminho(no_inicial, destinos, grid)
        tempo_total_execucao_astar += tempo_execucao_astar  # Somar o tempo de execução ao tempo total

        if not path:
            print("Nenhum caminho encontrado para os amigos restantes")
            return
        for i, (x, y) in enumerate(path):
            if (x, y) in amigos_nao_visitados:
                proximo_amigo = (x, y)
                proximo_caminho = path[:i+1]
                break
        path_total.extend(proximo_caminho)
        if proximo_amigo in amigos_aceitos:
            print(f"Convencido: ({proximo_amigo[0]}, {proximo_amigo[1]})")
        else:
            print(f"Recusado: ({proximo_amigo[0]}, {proximo_amigo[1]})")
        amigos_nao_visitados.remove(proximo_amigo)
        no_inicial = Node(proximo_amigo[0], proximo_amigo[1], grid[proximo_amigo[1]][proximo_amigo[0]])
    return_home = Node(19, 23, grid[23][19])
    path, tempo_execucao_astar = encontrar_caminho(no_inicial, [return_home], grid)
    tempo_total_execucao_astar += tempo_execucao_astar  # Somar o tempo de execução ao tempo total
    if path:
        path_total.extend(path)
    else:
        print("Nenhum caminho encontrado de volta para casa")
    print(f"Tempo total de execução do A*: {tempo_total_execucao_astar:.4f} segundos")
    desenhar_caminho(path_total, 50, None, amigos_aceitos, tempo_total_execucao_astar)

def desenhar_caminho(path, delay=50, amigo=None, amigos_aceitos=[], tempo_total_execucao_astar=0, status_amigos=[]):
    total_cost = 0
    start_time = time.time()
    plt.ion()
    fig = plt.figure(figsize=(14, 7))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
    ax = plt.subplot(gs[0])
    console_ax = plt.subplot(gs[1])
    exibir_mapa_interativo(grid, ax)
    amigos_text = f"Amigos Aceitos: {', '.join(f'({x}, {y})' for x, y in amigos_aceitos)}"
    console_ax.set_xlim(0, 1)
    console_ax.set_ylim(0, 1)
    console_ax.axis("off")
    console_texts = {
        "amigos": console_ax.text(0.05, 0.95, amigos_text, fontsize=8, color='black', weight='bold'),
        "movimento": console_ax.text(0.05, 0.85, "", fontsize=8, color='black'),
        "tempo": console_ax.text(0.05, 0.75, "", fontsize=8, color='black'),
        "custo_total": console_ax.text(0.05, 0.65, "", fontsize=8, color='black'),
        "execucao": console_ax.text(0.05, 0.55, f"Tempo total de execução do A*: {tempo_total_execucao_astar:.4f} segundos", fontsize=8, color='blue')
    }
    status_y = 0.45
    for status in status_amigos:
        console_ax.text(0.05, status_y, status, fontsize=8, color='orange')
        status_y -= 0.05

    amigos_visitados = set()
    for index, (x, y) in enumerate(path):
        casa_atual = grid[y][x]
        total_cost += terreno_custo[casa_atual]
        console_texts["movimento"].set_text(f"Movendo para ({x}, {y}) - Custo acumulado: {total_cost}")
        elapsed_time = time.time() - start_time
        console_texts["tempo"].set_text(f"Tempo de Execução: {elapsed_time:.2f} segundos")
        console_texts["custo_total"].set_text(f"Custo Total: {total_cost}")
        if (x, y) in amigos_aceitos and (x, y) not in amigos_visitados:
            status_amigo = f"Convencido: ({x}, {y})"
            console_ax.text(0.05, status_y, status_amigo, fontsize=8, color='orange')
            amigos_visitados.add((x, y))
            status_y -= 0.05
        elif (x, y) not in amigos_aceitos and (x, y) not in amigos_visitados and (x, y) in [amigo for amigo in amigos if amigo not in amigos_aceitos]:
            status_amigo = f"Recusado: ({x}, {y})"
            console_ax.text(0.05, status_y, status_amigo, fontsize=8, color='orange')
            amigos_visitados.add((x, y))
            status_y -= 0.05
        ax.scatter(x + 0.5, (len(grid) - y) - 0.5, color='pink', s=10)
        plt.draw()
        plt.pause(0.00001) 
    plt.ioff()
    plt.show()

def exibir_mapa_interativo(mapa, ax):
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            valor = mapa[i][j]
            cor = obter_cor(valor)
            rect = plt.Rectangle([j, len(mapa) - i - 1], 1, 1, facecolor=cor)
            ax.add_patch(rect)
    ax.set_xlim(0, len(mapa[0]))
    ax.set_ylim(0, len(mapa))
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')

def obter_cor(valor):
    if valor == 0:
        return 'orange'
    elif valor == 1:
        return 'gray'
    elif valor == 3:
        return 'brown'
    elif valor == 5:
        return 'green'
    elif valor == 10:
        return 'white'
    else:
        return 'black'

if __name__ == "__main__":
    grid = carregar_arquivo("mapaOficial.txt")
    no_inicial = Node(19, 23, grid[23][19])
    amigos = [(13, 5), (9, 10), (15, 36), (35, 6), (38, 24), (37, 37)]
    amigos_aceitos = AmigosAceitos()
    escolha = input("Deseja sortear os amigos aceitos (1) ou definir manualmente (2)? ")

    if escolha == "1":
        amigos_aceitos.sortear(amigos)
    elif escolha == "2":
        amigos_aceitos_manual = [(35, 6), (38, 24), (37, 37)]
        amigos_aceitos.definir(amigos_aceitos_manual)

    amigos_aceitos_lista = amigos_aceitos.amigos_aceitos
    amigos_aceitos_str = ', '.join(f'({x}, {y})' for x, y in amigos_aceitos_lista)
    print(f"Amigos Aceitos: {amigos_aceitos_str}")

    visitar_amigos(no_inicial, amigos_aceitos_lista, grid)

