from pydantic import BaseModel
from typing import Optional
import json
#import networkx

'''
Parse Graph to unified interior format


'''
LITEGRAPH_NAME_MAPPING: dict[str,str]= {
    'type' : 'model_name',
    'outputs': 'needs'
}

class Inputs(BaseModel):
    links: list[int]
    type: str

class Element(BaseModel):
    type: str 
    inputs: Optional[list[Inputs]] = None
    properties: Optional[dict[str,str]] = None 

class Graph(BaseModel):
    nodes: Optional[list[Element]] = None

def to_sequential(j: str | dict):
    '''
    In that format all

    Such format is beneficial for schedulers
    like Airflow or Gitlab CI, because they grab
    results of previous actions  

    Algorithm is simple.
    Collect all nodes. Take only outputs and collect
    nx.DiGraph.

    Perform topological sort over nodes
    '''

    if isinstance(j, str):
        model:dict = json.loads(j)
    elif isinstance(j, dict):
        model = j
    else:
        raise Exception('Inappropriate Format')
    
    return Graph(**model)

