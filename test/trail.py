import yaml
import collections
from functools import reduce
import networkx as nx
import random


class Node:
    def __init__(self,id):
        self.id = id
        self.color = random.choice(['red,blue']) 
        self.predecessors: list['Node'] = []

        def add_pred(self, node: 'Node'):
            self.predecessors.append(node)


nodes = {i:Node(i) for i in range(8)}

G: nx.DiGraph = nx.path_graph(6,create_using=nx.DiGraph)
G.add_edge(6,3)
for node in nx.topological_sort(G):
    for pred in G.predecessors(node):
        nodes[node].append(pred)


def from_generator(arg):
    return reduce(lambda x,y: x|y,(arg))

#print(from_generator({i: "dog"} for i in range(10)))

# with open('./default.yaml','r') as f: 
#     print(yaml.safe_load(f.read()))