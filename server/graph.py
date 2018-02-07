import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
DG = nx.DiGraph()
DG.add_weighted_edges_from([('amarshalkin', 'infom', 200), ('klimov', 'amarshalkin', 300), ('fedorov', 'amarshalkin', 150), ('fedorov', 'klimov', 50)])
nx.draw(DG, with_labels=True, font_weight='bold')
plt.savefig("graph.png")

simple = list(nx.simple_cycles(DG))

print(simple)
