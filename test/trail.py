from functools import reduce
from dataclasses import dataclass
import networkx as nx
import random
import inspect


for i in range(10):
    try:
        print(1/i)
    except ZeroDivisionError as e:
        print('Нельзя делить на ноль')

# with open('./default.yaml','r') as f:
#     print(yaml.safe_load(f.read()))


# NODE_PY_VIS = {
#     "Example": Cat


# }
# import inspect
# [m[0] for m in inspect.getmembers(my_module, inspect.isclass) if m[1].__module__ == 'my_module']

# # A dictionary that contains the friendly/humanly readable titles for the nodes
# NODE_DISPLAY_NAME_MAPPINGS = {
#     "Example": "Example Node"
# }