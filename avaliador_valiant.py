import random
import math
import matplotlib.pyplot as plt
from grafolib import Grafo
from algoritmo_valiant import algoritmo_valiant

# Gera grafo aleatório com m ≈ c * n * log(n) arestas
def gerar_grafo_aleatorio(n, c, arquivo_saida):
    arestas = set()
    max_arestas = n * (n - 1) // 2
    m = min(int(c * n * math.log(n)), max_arestas)
    # print(f"n = {n}, c = {c} → gerando m = {m} arestas")  # monitorar
    while len(arestas) < m:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            arestas.add((min(u, v), max(u, v)))
    with open(arquivo_saida, "w") as f:
        f.write(f"{n}\n")
        for u, v in arestas:
            f.write(f"{u} {v}\n")

# Executa o algoritmo várias vezes e calcula a taxa de sucesso
def testar_valiant_em_n_rodadas(n, c, rodadas=10):
    sucesso = 0
    for i in range(rodadas):
        gerar_grafo_aleatorio(n, c, "grafo_temp.txt")
        g = Grafo(directed=False, representation="list")
        g.load_from_file("grafo_temp.txt")
        ok, _ = algoritmo_valiant(g)
        if ok:
            sucesso += 1
    taxa_sucesso = sucesso / rodadas
    print(f"Resultado: n = {n}, c = {c}, Sucesso = {taxa_sucesso*100:.1f}%")
    return taxa_sucesso * 100

# Execução principal
if __name__ == "__main__":
    tamanhos = [100, 200, 400, 800]
    cs = [1, 3, 5, 7, 10]

    resultados_sucesso = {n: [] for n in tamanhos}

    for n in tamanhos:
        print(f"\nTestando para n = {n}")
        for c in cs:
            taxa = testar_valiant_em_n_rodadas(n, c)
            resultados_sucesso[n].append(taxa)

    # Gráfico: Taxa de Sucesso
    plt.figure(figsize=(10, 6))
    for n in tamanhos:
        plt.plot(cs, resultados_sucesso[n], label=f'n = {n}', marker='o')
    plt.xlabel("Valor de c (densidade)")
    plt.ylabel("Taxa de sucesso (%)")
    plt.title("Taxa de sucesso do algoritmo de Angluin & Valiant")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("grafico_taxa_sucesso.png")
    plt.show()
