from pydanticGraph import sequential_groups, format_to_yaml_groups
import json

with open("graph.json", "r") as f:
    j = json.loads(f.read())["body"]
    groupped_dag, g = sequential_groups(j)
    # print(groupped_dag, g)
    print(format_to_yaml_groups(groupped_dag, g))
