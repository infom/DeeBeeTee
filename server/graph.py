import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

DG = nx.DiGraph()
DG.add_weighted_edges_from([('amarshalkin', 'infom', 200), ('klimov', 'amarshalkin', 300), ('amarshalkin', 'fedorov', 150), ('fedorov', 'klimov', 50)])
nx.draw(DG, with_labels=True, font_weight='bold')
plt.savefig("graph.png")

print(list(find_cycle(DG, orientation='ignore')))
