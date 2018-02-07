import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

DG = nx.DiGraph()
DG.add_weighted_edges_from([('amarshalkin', 'infom', 200), ('klimov', 'amarshalkin', 300), ('amarshalkin', 'fedorov', 150), ('fedorov', 'klimov', 50)])
plt.subplot(211)
nx.draw(DG, with_labels=True, font_weight='bold')

G = nx.MultiDiGraph()
G.add_weighted_edges_from([('amarshalkin', 'infom', 200), ('klimov', 'amarshalkin', 300), ('amarshalkin', 'fedorov', 150), ('fedorov', 'klimov', 50)])
plt.subplot(212)
nx.draw(G, with_labels=True, font_weight='bold')

plt.savefig("graphs.png")
