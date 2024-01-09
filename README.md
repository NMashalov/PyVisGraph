# PydanticGraph
Organizing [Pydantic](https://github.com/jagenjo/litegraph.js/tree/master) models into graph with [Litegraph](https://github.com/jagenjo/litegraph.js/tree/master) interface.


## Quick start

```
poetry shell # creates virtual environment for project
poetry install # 
```

## Functionality 
- flexible organization nodes defined via pydantic models
- transform graph to yaml and yaml to graph  


## Adding custom model

```python
from pydanticGraph import Node
from pydantic import Field

class MyScoring(Node):
    # will be displayed in widget
    class Widget:
        model_name: str  = Field(description="Write path to model ") # add description to your . They will be displayed in UI
        threshold: float  = Field(description="Write threshold from 0 to 1")
    class Input:
        : int
    class Outputs:
        
```
## Configurate yaml of Graph 
Can be configured with [`graph.conf.yaml`](graph.conf.yaml).


## Intro image

## Docs


## References
- [Litegraph](https://github.com/jagenjo/litegraph.js/tree/master)
- [Pydantic](https://github.com/jagenjo/litegraph.js/tree/master)
