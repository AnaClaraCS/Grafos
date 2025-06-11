from grafolib import Grafo

# Caso 1: Grafo esparso

g = Grafo(representation="list")
g.load_from_file("grafo_esparso.txt")
g.write_info("saida_info_esparso.txt")
g.bfs(0, "saida_bfs_esparso.txt")
g.dfs(0, "saida_dfs_esparso.txt")
g.connected_components("saida_componentes_esparso.txt")

# Caso 2: Grafo denso

g = Grafo(representation="matrix")
g.load_from_file("grafo_denso.txt")
g.write_info("saida_info_denso.txt")
g.bfs(0, "saida_bfs_denso.txt")
g.dfs(0, "saida_dfs_denso.txt")
g.connected_components("saida_componentes_denso.txt")
