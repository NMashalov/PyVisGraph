from pyvisgraph import format_dag_to_groups, Dag 
import json

with open("graph.json", "r") as f:
    j = json.loads(f.read())["body"]
    g = Dag(**j)
    print(format_dag_to_groups(g))
