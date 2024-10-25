import heapq
import random
import time
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# Tamanho do tile
tile_size = 20

# Variáveis globais
grid = []  # Armazena o grid carregado
amigos_aceitos = []  # Armazena os amigos que aceitarão o convite
start_node = None  # Posição inicial da Barbie

# Dicionário de custo por tipo de terreno
terreno_custo = {
    5: 5,        # Grama
    1: 1,        # Asfalto
    3: 3,        # Terra
    10: 10,      # Paralelepípedo
    0: float("inf"),  # Edifícios (intransponível)
    2: 2         # Outro tipo de terreno, se necessário
}

grid_state = []  # Armazena o estado original do grid (as cores)

# Localização dos amigos
amigos = [
    (13, 5), 
    (9, 10), 
    (15, 36), 
    (35, 6), 
    (38, 24), 
    (37, 37) 
]

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

# Sortear amigos aceitos
def sortear_amigos_aceitos():
    global amigos_aceitos
    if not amigos_aceitos:
        amigos_aceitos = random.sample(amigos, 3)
    return amigos_aceitos

# Definir amigos aceitos manualmente
def definir_amigos_aceitos(manual_amigos):
    global amigos_aceitos
    amigos_aceitos = manual_amigos
    return amigos_aceitos


def load_grid_from_file(file):
    with open(file, "r") as f:
        data = f.read().strip().split("\n")
        return [list(map(int, line.strip().split(','))) for line in data]

def calcular_heuristica(ponto_atual, destinos):
    return min(abs(ponto_atual[0] - destino.x) + abs(ponto_atual[1] - destino.y) for destino in destinos)

def astar(start, destinos, grid):
    open_list = MinHeap()
    closed_set = set()
    destino_coords = [(destino.x, destino.y) for destino in destinos]
    
    start.g = 0
    start.h = calcular_heuristica((start.x, start.y), destinos)
    start.f = start.g + start.h
    open_list.insert(start)
    
    while open_list.size() > 0:
        current_node = open_list.extract_min()
        if (current_node.x, current_node.y) in destino_coords:
            path = []
            temp = current_node
            while temp:
                path.append((temp.x, temp.y))
                temp = temp.parent
            return path[::-1]
        
        closed_set.add((current_node.x, current_node.y))
        
        neighbors = [
            (current_node.x + 1, current_node.y),
            (current_node.x - 1, current_node.y),
            (current_node.x, current_node.y + 1),
            (current_node.x, current_node.y - 1)
        ]
        
        for nx, ny in neighbors:
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                neighbor = Node(nx, ny, grid[ny][nx])
                if terreno_custo[neighbor.cost] == float("inf") or (neighbor.x, neighbor.y) in closed_set:
                    continue
                
                tentative_g = current_node.g + terreno_custo[neighbor.cost]
                if tentative_g < neighbor.g or (neighbor.x, neighbor.y) not in {n[1] for n in open_list.heap}:
                    neighbor.g = tentative_g
                    neighbor.h = calcular_heuristica((neighbor.x, neighbor.y), destinos)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current_node
                    open_list.insert(neighbor)
    
    return []  # Nenhum caminho encontrado

def visitar_amigos(start_node):
    global amigos_aceitos
    path_total = []
    amigos_nao_visitados = amigos.copy()
    amigos_convencidos = 0

    while amigos_convencidos < 3 and amigos_nao_visitados:
        destinos = [Node(amigo[0], amigo[1], grid[amigo[1]][amigo[0]]) for amigo in amigos_nao_visitados]
        path = astar(start_node, destinos, grid)
        
        if not path:
            print("Nenhum caminho encontrado para os amigos restantes")
            return

        # Encontrar o próximo amigo com menor custo
        for i, (x, y) in enumerate(path):
            if (x, y) in amigos_nao_visitados:
                proximo_amigo = (x, y)
                proximo_caminho = path[:i+1]
                break
        
        path_total.extend(proximo_caminho)
        if proximo_amigo in amigos_aceitos:
            amigos_convencidos += 1
            print(f"Convencido: ({proximo_amigo[0]}, {proximo_amigo[1]})")
        else:
            print(f"Recusado: ({proximo_amigo[0]}, {proximo_amigo[1]})")
        
        amigos_nao_visitados.remove(proximo_amigo)
        start_node = Node(proximo_amigo[0], proximo_amigo[1], grid[proximo_amigo[1]][proximo_amigo[0]])

    return_home = Node(19, 23, grid[23][19])
    path = astar(start_node, [return_home], grid)
    if path:
        path_total.extend(path)
    else:
        print("Nenhum caminho encontrado de volta para casa")

    animate_path(path_total, 50, None, True)


def animate_path(path, delay=50, amigo=None, returning=False):
    total_cost = 0
    start_time = time.time()
    
    plt.ion()
    fig = plt.figure(figsize=(14, 12))  # Aumentar a altura da figura para acomodar o texto abaixo
    
    # Dividir a figura em duas partes, uma para o mapa e outra para o console
    gs = gridspec.GridSpec(3, 1, height_ratios=[4, 1, 0.5])  # Ajustar os ratios para espaço do console
    
    ax = plt.subplot(gs[0])
    console_ax = plt.subplot(gs[1])
    status_ax = plt.subplot(gs[2])
    
    exibir_mapa_interativo(grid, ax)  # Mostrar o mapa apenas uma vez
    
    amigos_text = f"Amigos Aceitos: {amigos_aceitos}"
    
    console_ax.set_xlim(0, 1)
    console_ax.set_ylim(0, 1)
    console_ax.axis("off")
    
    status_ax.set_xlim(0, 1)
    status_ax.set_ylim(0, 1)
    status_ax.axis("off")
    
    console_texts = {
        "amigos": console_ax.text(0.05, 0.9, amigos_text, fontsize=8, color='black', weight='bold'),
        "movimento": console_ax.text(0.05, 0.7, "", fontsize=8, color='black'),
        "tempo": console_ax.text(0.05, 0.5, "", fontsize=8, color='black'),
        "custo_total": console_ax.text(0.05, 0.3, "", fontsize=8, color='black'),
        "aceitacao": status_ax.text(0.05, 0.1, "", fontsize=8, color='orange')  # Exibir aceitação abaixo
    }
    
    original_values = {}
    aceitou_amigos = set()

    for index, (x, y) in enumerate(path):
        # Armazenar o custo da célula atual
        if (x, y) not in original_values:
            original_values[(x, y)] = grid[y][x]
        casa_atual = original_values[(x, y)]
        total_cost += terreno_custo[casa_atual]
        
        # Atualizar o console
        console_texts["movimento"].set_text(f"Movendo para ({x}, {y}) - Custo acumulado: {total_cost}")
        elapsed_time = time.time() - start_time
        console_texts["tempo"].set_text(f"Tempo de Execução: {elapsed_time:.2f} segundos")
        console_texts["custo_total"].set_text(f"Custo Total: {total_cost}")

        # Verificar se chegou em um amigo e mostrar se aceitou
        if (x, y) in amigos and (x, y) not in aceitou_amigos:
            status = "Aceitou" if (x, y) in amigos_aceitos else "Não aceitou"
            aceitou_amigos.add((x, y))
            aceitou_text = f"Amigo em ({x}, {y}): {status}"
            console_texts["aceitacao"].set_text(f"{console_texts['aceitacao'].get_text()}\n{aceitou_text}")

        # Marcar a célula como ocupada
        grid[y][x] = 100
        
        # Ajustar a posição do ponto para mostrar o rastro
        ax.scatter(x + 0.5, (len(grid) - y) - 0.5, color='pink', s=10)
        
        if index % 10 == 0:  # Atualizar o gráfico a cada 10 passos
            plt.draw()  # Atualizar a figura sem fechar
        
        plt.pause(0.00001)  # Diminuir o tempo de pausa
    
    # Restaurar os valores originais das células
    for (x, y), valor in original_values.items():
        grid[y][x] = valor
    
    plt.ioff()
    plt.show()
    
    if amigo:
        console_texts["custo_total"].set_text(f"Encontrou amigo: ({amigo[0]}, {amigo[1]}) - Custo total: {total_cost}")
    elif returning:
        console_texts["custo_total"].set_text(f"Retornou para casa - Custo total: {total_cost}")


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
    elif valor == 100:
        return 'pink'
    else:
        return 'black'

if __name__ == "__main__":
    grid = load_grid_from_file("mapa2.txt")
    start_node = Node(19, 23, grid[23][19])
    
    # Escolha entre sorteio ou definição manual
    escolha = input("Deseja sortear os amigos aceitos (1) ou definir manualmente (2)? ")
    
    if escolha == "1":
        sortear_amigos_aceitos()
    elif escolha == "2":
        amigos_aceitos_manual = [
            (13, 5), 
            (9, 10), 
            (15, 36)
        ]
        definir_amigos_aceitos(amigos_aceitos_manual)
    else:
        print("Escolha inválida. Sorteando amigos.")
        sortear_amigos_aceitos()
    
    print("Amigos Aceitos:", amigos_aceitos)
    visitar_amigos(start_node)



