import matplotlib.pyplot as plt
import random
import heapq
import math

barbie = (23, 19)
amigos = [
    (5, 13), 
    (10, 9), 
    (36, 15), 
    (6, 35), 
    (24, 38), 
    (37, 37) 
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
    fig, ax = plt.subplots()
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            valor = mapa[i][j]
            cor = obter_cor(valor)
            rect = plt.Rectangle([j, len(mapa) - i - 1], 1, 1, facecolor=cor)
            ax.add_patch(rect)
    plt.xlim(0, len(mapa[0]))
    plt.ylim(0, len(mapa))
    plt.gca().set_aspect('equal', adjustable='box')  
    plt.axis('off')  
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
        exibir_mapa(mapa) 
        mapa [x][y] = casa_atual
    return mapa

# Sorteio amigos que responderão SIM
def sortear_amigos(qtd):
    return random.sample(amigos, qtd)


# Cálculo da menor heurística com base na distância Manhattan para qualquer destino
def calcular_heuristica(ponto_atual, destinos):
    return min(abs(ponto_atual[0] - destino[0]) + abs(ponto_atual[1] - destino[1]) for destino in destinos)


# Algoritmo A*
def calcular_astar(mapa, inicio, destinos):
    # Fronteira (Fila de prioridade)
    fronteira = []
    heapq.heappush(fronteira, (0, inicio))

    # Mapear de onde viemos e o custo até agora
    veio_de = {}
    custo_ate_aqui = {}
    veio_de[inicio] = None
    custo_ate_aqui[inicio] = 0

    while fronteira:
        # Pega o ponto de menor custo estimado da fronteira
        _, ponto_atual = heapq.heappop(fronteira)

        # Se chegamos ao último destino, terminamos
        if ponto_atual in destinos:
            destinos.remove(ponto_atual)  # Remove destino da lista
            if not destinos:  # Se visitamos todos os destinos
                break

        # Movimentos possíveis (cima, baixo, esquerda, direita)
        movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for movimento in movimentos:
            vizinho = (ponto_atual[0] + movimento[0], ponto_atual[1] + movimento[1])

            # Verifica se o vizinho está dentro dos limites do mapa
            if 0 <= vizinho[0] < len(mapa) and 0 <= vizinho[1] < len(mapa[0]):
                terreno = mapa[vizinho[0]][vizinho[1]]
                # Verifica se é um terreno acessível (diferente de 0)
                if terreno < 999999999:  # Apenas terrenos com custo maior que 0 são acessíveis
                    novo_custo = custo_ate_aqui[ponto_atual] + terreno
                    # Se o custo do vizinho for menor ou não existe, atualize
                    if vizinho not in custo_ate_aqui or novo_custo < custo_ate_aqui[vizinho]:
                        custo_ate_aqui[vizinho] = novo_custo
                        prioridade = novo_custo + calcular_heuristica(vizinho, destinos)
                        heapq.heappush(fronteira, (prioridade, vizinho))
                        veio_de[vizinho] = ponto_atual
                else:
                    print(f"Vizinho {vizinho} com custo {terreno} ignorado (edifício).")

            # Dentro do loop que verifica vizinhos
            print(f"Verificando vizinho: {vizinho} com custo: {terreno}")

    if destinos:
        print("Erro: Nenhum destino possível encontrado.")
    else:
        print("Todos os destinos foram alcançados.")
    return veio_de, custo_ate_aqui
    

# Função para reconstruir o caminho baseado no dicionário veio_de
def reconstruir_caminho(veio_de, inicio, final):
    caminho = []
    ponto_atual = final
    while ponto_atual != inicio:
        caminho.append(ponto_atual)
        ponto_atual = veio_de[ponto_atual]
    caminho.append(inicio)  # Adicionar o ponto de início no final
    caminho.reverse()  # Inverter o caminho para ficar do início ao final
    return caminho

def calcular_percurso_barbie(mapa, barbie, amigos):
    todos_destinos = amigos 
    gambi = amigos
    
    
    percurso_completo = []

    # Barbie começa na posição inicial e visita todos os amigos
    posicao_atual = barbie
    while todos_destinos:
        # Calcula o A* do ponto atual até o próximo destino mais próximo
        veio_de, custo_ate_aqui = calcular_astar(mapa, posicao_atual, gambi)


        input("Pressione Enter para continuar...")


        # Verifique se custo_ate_aqui está preenchido e se há destinos válidos
        if custo_ate_aqui:
            destinos_validos = [destino for destino in todos_destinos if destino in custo_ate_aqui]

            
            if destinos_validos:
                destino_mais_proximo = min(destinos_validos, key=lambda destino: custo_ate_aqui[destino])
            else:
                print("Erro: Nenhum destino possível encontrado.")
                break
        else:
            print("Erro: custo_ate_aqui está vazio.")
            break
        
        # Reconstrói o caminho até o próximo destino
        caminho = reconstruir_caminho(veio_de, posicao_atual, destino_mais_proximo)
        percurso_completo.extend(caminho)  # Adiciona o caminho ao percurso completo

        # Atualiza a posição atual e remove o destino da lista
        posicao_atual = destino_mais_proximo
        todos_destinos.remove(destino_mais_proximo)

    return percurso_completo















# percurso = [(23, 20),(23, 21), (22, 21), (21, 21), (20, 21)]

# Arquivo do qual a matriz será carregada
arquivo_txt = 'mapa.txt'

# Sortear 3 amigos
amigos_sorteados = sortear_amigos(3)
print(amigos_sorteados)

# Definição dos 3 amigos de forma manual
amigos_manual =  [
    (5, 13), # amigo 1
    (10, 9), # amigo 2
    (36, 15), # amigo 3
    (6, 35), # amigo 4
    (24, 38), # amigo 5
    (37, 37) # amigo 6
]



# Carregar a matriz e exibir o mapa
mapa = carregar_matriz(arquivo_txt)
mapa = definir_posicao_personagens(mapa)
# mapa = exibir_percurso (mapa, percurso)
# exibir_mapa(mapa)
# Chamando a função para calcular o percurso completo

percurso_barbie = calcular_percurso_barbie(mapa, barbie, amigos)
# Exibir o percurso no mapa
mapa = exibir_percurso(mapa, percurso_barbie)