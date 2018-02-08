import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

array1 = [('amarshalkin', 'infom', 200), ('klimov', 'amarshalkin', 300), ('amarshalkin', 'fedorov', 150), ('fedorov', 'klimov', 50)]
array2 = [('amarshalkin', 'infom', 200),('infom', 'amarshalkin', 100), ('klimov', 'amarshalkin', 300), ('amarshalkin', 'fedorov', 150), ('fedorov', 'klimov', 50), ('klimov', 'fedorov', 150)]
array3 = [('amarshalkin', 'infom'), ('klimov', 'amarshalkin'), ('amarshalkin', 'fedorov'), ('fedorov', 'klimov')]

# Create direct Graph
DG = nx.DiGraph()
DG.add_weighted_edges_from(array1)
pos=nx.shell_layout(DG) # positions for all nodes

ax = plt.subplot(111)
ax.set_title("Direct Graph")

# Find simple direct cycle
sc = list(nx.simple_cycles(DG))

# Draw Direct Graph and simple sycle
nx.draw_shell(DG, with_labels=True, font_weight='bold')
for cycle in sc:
    print('find simple cycle from direct graph:', cycle)
    nx.draw_networkx_nodes(DG,pos,
                       nodelist=cycle,
                       node_color='b',
                       alpha=1)


# Create Multi Direct Graph
MDG = nx.MultiDiGraph()
MDG.add_weighted_edges_from(array2)
pos=nx.shell_layout(MDG)

ax1 = plt.subplot(121)
ax1.set_title("Multi Direct Graph")

# Find simple multi direct cycle
sc = list(nx.simple_cycles(MDG))

# Draw Direct Graph and simple sycle
nx.draw_shell(MDG, with_labels=True, font_weight='bold')
for cycle in sc:
    print('find simple cycle from multi direct graph:', cycle)
    nx.draw_networkx_nodes(MDG,pos,
                       nodelist=cycle,
                       node_color='g',
                       alpha=1)

# Create Graph
G = nx.Graph()
G.add_weighted_edges_from(array1)

ax1 = plt.subplot(131)
ax1.set_title("Graph")

# Draw Graph
nx.draw_shell(G, with_labels=True, font_weight='bold')

plt.savefig("static/img/graphs.png", dpi=300)
