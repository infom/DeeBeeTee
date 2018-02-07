import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

DG = nx.DiGraph()
DG.add_weighted_edges_from([('amarshalkin', 'infom', 200), ('klimov', 'amarshalkin', 300), ('amarshalkin', 'fedorov', 150), ('fedorov', 'klimov', 50)])
pos=nx.shell_layout(DG) # positions for all nodes

ax = plt.subplot(211)
ax.set_title("Direct Graph")
sc = list(nx.simple_cycles(DG))

nx.draw_shell(DG, with_labels=True, font_weight='bold')
for cycle in sc:
    nx.draw_networkx_nodes(DG,pos,
                       nodelist=cycle,
                       node_color='b',
                       alpha=1)



G = nx.MultiDiGraph()
G.add_weighted_edges_from([('amarshalkin', 'infom', 200),('infom', 'amarshalkin', 100), ('klimov', 'amarshalkin', 300), ('amarshalkin', 'fedorov', 150), ('fedorov', 'klimov', 50), ('klimov', 'fedorov', 150)])
pos=nx.shell_layout(G)

ax1 = plt.subplot(212)
ax1.set_title("Multi Direct Graph")
sc = list(nx.simple_cycles(G))

nx.draw_shell(G, with_labels=True, font_weight='bold')
for cycle in sc:
    nx.draw_networkx_nodes(G,pos,
                       nodelist=cycle,
                       node_color='b',
                       alpha=1)

plt.savefig("graphs.png")



# nodes
