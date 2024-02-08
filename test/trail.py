from functools import reduce
from dataclasses import dataclass
import networkx as nx
import random

net: nx.DiGraph = nx.path_graph(6, create_using=nx.DiGraph)
nx.set_node_attributes(net,'red',"color")



for node in nx.topological_sort(net):
    print(node)
# with open('./default.yaml','r') as f:
#     print(yaml.safe_load(f.read()))
