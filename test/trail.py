import yaml

with open('./default.yaml','r') as f: 
    print(yaml.safe_load(f.read()))