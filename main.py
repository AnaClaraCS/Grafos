from grafolib import Grafo

# Instanciando o grafo com pesos
g = Grafo(representation="list", weighted=True)

# Carrega o grafo
g.load_from_file("grafoComPeso.txt")

# Gera o arquivo de informações do grafo
g.write_info("saida_info.txt")

# Faz busca em largura e salva
g.bfs_to_file(0, "saida_bfs.txt")

# Faz busca em profundidade e salva
g.dfs_to_file(0, "saida_dfs.txt")

# Parte 2

# Calcula caminho mínimo entre dois vértices
g.caminho_minimo(0, 3, "saida_caminho.txt")

# Calcula o caminho minimo de um vértico com os outros do grafo
g.caminho_minimo_todos(0, "saida_caminho_todos.txt")
