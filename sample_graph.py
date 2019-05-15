import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
G = nx.Graph()
vlist = [1, 2, 3, 4, 5, 6]
elist = [(2, 1), (1, 3), (2, 3), (2, 4), (3, 4), (5, 6), (1, 6), (6, 3), (5, 2)]
G.add_nodes_from(vlist)
G.add_edges_from(elist)
nx.draw_networkx(G, node_color='lightgray', node_size=400)
plt.axis('off')
plt.show()