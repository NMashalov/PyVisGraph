from pydanticGraph import to_sequential

with open('graph.json','r') as f: 
    j =   f.read()
    to_sequential(j)
