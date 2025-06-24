from collections import defaultdict, deque
import heapq

class Grafo:

    # Inicializa o grafo com a representeção escolhida e os outros atributos como vazio
    def __init__(self, directed=False, representation="list", weighted=False):
        self.directed = directed
        self.repr = representation
        self.weighted = weighted
        self.n = 0
        self.lista = defaultdict(list)
        self.matriz = []
        self.arestas = []
        self.pesos = dict()

    # Realiza a leitura de um arquivo .txt e converte em um grafo com a representação escolhida
    def load_from_file(self, arquivo):
        with open(arquivo, "r") as f:
            linhas = f.readlines()
            self.n = int(linhas[0])
            self.arestas.clear()
            self.pesos.clear()
            for linha in linhas[1:]:
                partes = linha.strip().split()
                u, v = int(partes[0]), int(partes[1])
                peso = float(partes[2]) if self.weighted and len(partes) == 3 else 1.0
                self.arestas.append((u, v))
                # Adiciona o peso da aresta, se for um grafo com pesos
                self.pesos[(u, v)] = peso
                if not self.directed:
                    self.pesos[(v, u)] = peso
                # Trata o grafo como uma lista de adjacência
                if self.repr == "list":
                    self.lista[u].append(v)
                    if not self.directed:
                        self.lista[v].append(u)
                # Trata o grafo como uma matriz de adjacência
                elif self.repr == "matrix":
                    if not self.matriz:
                        self.matriz = [[0]*self.n for _ in range(self.n)]
                    self.matriz[u][v] = peso
                    if not self.directed:
                        self.matriz[v][u] = peso

    # Escreve as informações do grafo em um arquivo de saída
    def write_info(self, saida):
        graus = self._graus()
        total_arestas = len(self.arestas)
        grau_medio = sum(graus.values()) / self.n
        distribuicao_empirica = self._distribuicao_empirica()
        with open(saida, "w") as f:
            f.write(f"Número de vértices: {self.n}\n")
            f.write(f"Número de arestas: {total_arestas}\n")
            f.write(f"Grau médio: {grau_medio:.2f}\n")
            f.write("Distribuição empírica dos graus:\n")
            # Correção da parte 1
            for g in sorted(distribuicao_empirica):
                f.write(f"Grau {g}: {distribuicao_empirica[g]:.2f}\n")

    # Calcula os graus dos vértices
    def _graus(self):
        graus = defaultdict(int)
        if self.repr == "list":
            for v in self.lista:
                graus[v] = len(self.lista[v])
        elif self.repr == "matrix":
            for i in range(self.n):
                graus[i] = sum(self.matriz[i])
        return graus
    
    # Calcula a distribuição empírica dos graus
    def _distribuicao_empirica(self):
        graus = self._graus()
        distrib = defaultdict(int)
        for grau in graus.values():
            distrib[grau] += 1/ self.n
        return distrib

    # Realiza a busca em largura (BFS) a partir de um vértice inicial
    def bfs_to_file(self, inicio, arquivo_saida):
        visitado = [False]*self.n
        pai = [-1]*self.n
        nivel = [-1]*self.n
        dist = [-1]*self.n
        fila = deque()
        visitado[inicio] = True
        nivel[inicio] = 0
        dist[inicio] = 0
        fila.append(inicio)
        while fila:
            atual = fila.popleft()
            vizinhos = self.lista[atual] if self.repr == "list" else [
                j for j in range(self.n) if self.matriz[atual][j]]
            for viz in vizinhos:
                if not visitado[viz]:
                    visitado[viz] = True
                    pai[viz] = atual
                    nivel[viz] = nivel[atual] + 1
                    dist[viz] = dist[atual] + 1
                    fila.append(viz)
        with open(arquivo_saida, "w") as f:
            f.write("Vértice | Pai | Nível\n")
            for i in range(self.n):
                f.write(f"{i} {pai[i]} {nivel[i]}\n")
        return dist, pai # Retorna distância e pais para uso no caminho minimo

    # Realiza a busca em profundidade (DFS) a partir de um vértice inicial
    def dfs_to_file(self, inicio, arquivo_saida):
        visitado = [False]*self.n
        pai = [-1]*self.n
        nivel = [-1]*self.n

        def dfs_rec(v, d):
            visitado[v] = True
            nivel[v] = d
            vizinhos = self.lista[v] if self.repr == "list" else [
                j for j in range(self.n) if self.matriz[v][j]]
            for u in vizinhos:
                if not visitado[u]:
                    pai[u] = v
                    dfs_rec(u, d + 1)

        dfs_rec(inicio, 0)

        with open(arquivo_saida, "w") as f:
            f.write("Vértice | Pai | Nível\n")
            for i in range(self.n):
                f.write(f"{i} {pai[i]} {nivel[i]}\n")

    # Encontra os componentes conexos do grafo e escreve em um arquivo de saída
    def connected_components(self, arquivo_saida):
        visitado = [False]*self.n
        componentes = []

        def dfs_comp(v, comp):
            visitado[v] = True
            comp.append(v)
            vizinhos = self.lista[v] if self.repr == "list" else [
                j for j in range(self.n) if self.matriz[v][j]]
            for u in vizinhos:
                if not visitado[u]:
                    dfs_comp(u, comp)

        for v in range(self.n):
            if not visitado[v]:
                comp = []
                dfs_comp(v, comp)
                componentes.append(comp)

        componentes.sort(key=lambda c: len(c), reverse=True)
        with open(arquivo_saida, "w") as f:
            f.write(f"Número de componentes conexos: {len(componentes)}\n")
            for i, comp in enumerate(componentes):
                f.write(f"Componente {i+1} (tamanho {len(comp)}): {sorted(comp)}\n")

    # Realiza o algoritmo de Dijkstra para encontrar o caminho mínimo em um grafo com pesos
    def dijkstra(self, inicio):
        menor_peso = min(self.pesos.values(), default=0)
        ajuste = 0
        # Se tiver um peso negativo, ajusta para que todos os pesos sejam não-negativos
        if menor_peso < 0:
            ajuste = -menor_peso

        dist = [float('inf')]*self.n
        pai = [-1]*self.n
        dist[inicio] = 0
        heap = [(0, inicio)]

        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            vizinhos = self.lista[u] if self.repr == "list" else [
                j for j in range(self.n) if self.matriz[u][j] != 0]
            for v in vizinhos:
                peso = self.pesos.get((u, v), 1.0) + ajuste
                if dist[u] + peso < dist[v]:
                    dist[v] = dist[u] + peso
                    pai[v] = u
                    heapq.heappush(heap, (dist[v], v))

        # Remove o efeito do ajuste da distância final
        dist = [d - ajuste * self._conta_arestas(origem=inicio, destino=i, pai=pai) if d != float('inf') else d for i, d in enumerate(dist)]

        return dist, pai

    # Conta quantas arestas há entre origem
    def _conta_arestas(self, origem, destino, pai):
        if origem == destino:
            return 0
        cont = 0
        atual = destino
        while atual != -1 and atual != origem:
            atual = pai[atual]
            cont += 1
        return cont if atual != -1 else 0

    # Encontra o caminho mínimo entre dois vértices e escreve em um arquivo de saída
    def caminho_minimo(self, origem, destino, saida):
        if self.weighted:
            dist, pai = self.dijkstra(origem)
        else:
            dist, pai = self.bfs(origem)
        caminho = []
        atual = destino
        while atual != -1:
            caminho.append(atual)
            atual = pai[atual]
        caminho.reverse()
        with open(saida, "w") as f:
            f.write(f"Caminho mínimo de {origem} até {destino}: {caminho}\n")
            f.write(f"Distância: {dist[destino]}\n")

    # Encontra o caminho mínimo de um vértice ao demais do grafo
    def caminho_minimo_todos(self, origem, saida):
        if self.weighted:
            dist, pai = self.dijkstra(origem)
        else:
            dist, pai = self.bfs(origem)
        
        with open(saida, "w") as f:
            for destino in range(self.n):
                if dist[destino] == float('inf') or dist[destino] == -1:
                    f.write(f"Sem caminho de {origem} para {destino}\n")
                    continue
                caminho = []
                atual = destino
                while atual != -1:
                    caminho.append(atual)
                    atual = pai[atual]
                caminho.reverse()
                f.write(f"Caminho de {origem} até {destino}: {caminho} | Distância: {dist[destino]}\n")

