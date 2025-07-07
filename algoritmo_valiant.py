import random

def algoritmo_valiant(grafo, max_tentativas=100):
    n = grafo.n
    vertices = list(range(n))
    random.shuffle(vertices)
    
    ciclo = [vertices.pop()]  # começa com um vértice aleatório
    visitado = set(ciclo)

    tentativas = 0
    while len(visitado) < n and tentativas < max_tentativas:
        # Tenta inserir vértices ainda não visitados no ciclo atual
        inseriu = False
        for v in vertices[:]:  # percorre uma cópia da lista
            for i in range(len(ciclo)):
                u = ciclo[i]
                w = ciclo[(i + 1) % len(ciclo)]
                # tenta inserir v entre u e w
                if v in grafo.lista[u] and v in grafo.lista[w]:
                    ciclo.insert(i + 1, v)
                    visitado.add(v)
                    vertices.remove(v)
                    inseriu = True
                    break
            if inseriu:
                break
        if not inseriu:
            tentativas += 1

    # Verifica se o ciclo cobre todos os vértices e está fechado
    if len(ciclo) == n and ciclo[0] in grafo.lista[ciclo[-1]]:
        return True, ciclo + [ciclo[0]]
    else:
        return False, ciclo
