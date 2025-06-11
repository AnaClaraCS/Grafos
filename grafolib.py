from collections import defaultdict, deque

class Grafo:
    def __init__(self, directed=False, representation="list"):
        self.directed = directed
        self.repr = representation
        self.n = 0
        self.lista = defaultdict(list)
        self.matriz = []
        self.arestas = []

    def load_from_file(self, arquivo):
        with open(arquivo, "r") as f:
            linhas = f.readlines()
            self.n = int(linhas[0])
            self.arestas.clear()
            for linha in linhas[1:]:
                u, v = map(int, linha.strip().split()[:2])
                self.arestas.append((u, v))
                if self.repr == "list":
                    self.lista[u].append(v)
                    if not self.directed:
                        self.lista[v].append(u)
                elif self.repr == "matrix":
                    if not self.matriz:
                        self.matriz = [[0]*self.n for _ in range(self.n)]
                    self.matriz[u][v] = 1
                    if not self.directed:
                        self.matriz[v][u] = 1

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
            for g in sorted(distribuicao_empirica):
                f.write(f"Grau {g}: {distribuicao_empirica[g]:.2f}\n")

    def _graus(self):
        graus = defaultdict(int)
        if self.repr == "list":
            for v in self.lista:
                graus[v] = len(self.lista[v])
        elif self.repr == "matrix":
            for i in range(self.n):
                graus[i] = sum(self.matriz[i])
        return graus
    
    def _distribuicao_empirica(self):
        graus = self._graus()
        distrib = defaultdict(int)
        for grau in graus.values():
            distrib[grau] += 1/ self.n
        return distrib

    def bfs(self, inicio, arquivo_saida):
        visitado = [False]*self.n
        pai = [-1]*self.n
        nivel = [-1]*self.n
        fila = deque()
        visitado[inicio] = True
        nivel[inicio] = 0
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
                    fila.append(viz)
        with open(arquivo_saida, "w") as f:
            f.write("Vértice | Pai | Nível\n")
            for i in range(self.n):
                f.write(f"{i} {pai[i]} {nivel[i]}\n")

    def dfs(self, inicio, arquivo_saida):
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
