# PyVisGraph
Visual connecting Python classes in Directed Acyclic Graphs using [Litegraph](https://github.com/jagenjo/litegraph.js/tree/master) interface.

![Demo.jpg](assets/ui.png)

## Introduction

Start requires some work

1. Add to your class variables INPUT and OUTPUT in format ("arbitray node name","extension")
    ```python
    from typing import ClassVar
    class Myclass:
        INPUT: ClassVar =  ("Data", ".csv")
        OUTPUT: ClassVar = ("Model", ".pickle")

        # your init arguments will be properties of model
        def __init__(self, my_awesome_arg: int):
            # type will be converted. Use planar input int, string, float and etc
            ...

    class InferenceClass:
        # several inputs and ouputs are allowed
        INPUT: list[ClassVar] =  [("Data", ".csv"),("Model", ".csv")]
        OUTPUT: ClassVar = [("Data", ".csv")]

    ```

    LiteGraph will make sure, that you won't connect input and output with unequal extensions.
2. Install everything you need
    ```bash
    git clone https://github.com/NMashalov/PyVisGraph# clone repo with git 
    poetry shell # creates virtual environment for project
    poetry install # install all dependencies
    pyvisgraph start # load example 
    ```
3. (Optional) Customize `.py-vis-graph-preset.yaml` to your needs
    ```yaml
    import_paths:
    - module_name: scoring
      import_paths: ./test/nodes.py
    - module_name: scoring
      import_paths: ./test/nodes.py
    preset:
        output_settings:
            format: yaml
            mode: groupped
            dependency_name: needs
        graph_info:
            name: MyDag 
            group_name: "group"
            task_name: "task"
            properties:
            schedule: '0 * * * *'    
    ```

Demo via [link](nmashalov.github.io/Pydantic_litegraph/)

## Quick start 🎈


You can add your own model by just simple dropping of `.py` file with models.

### Functionality
- flexible organization of nodes defined via pydantic models
- transform LiteGraph linkage to Gitlab style aka `depends_on`

### Features 🧰
- Use buttons `validate` and `download` for checking your workflow
- New nodes can be added via dropping `.py` file to canvas.
- Docstring and Pydantic fields description forms hint 
![hint](assets/features/hint.png)

## Adding custom model
For defining models you need only pydantic.

Upload can be performed in several convenient way.
- explicitly define path

## Configurate yaml of Graph 
Can be configured with [`graph.conf.yaml`](graph.conf.yaml).

## Modifications

Under the hood of module is client-server with FastApi. This helps to couple Javascript and Python.  

All modifications can be performed as simple as 

## References
- [FastApi](https://fastapi.tiangolo.com/)
- [Litegraph](https://github.com/jagenjo/litegraph.js/tree/master)
- [Pydantic](https://docs.pydantic.dev/latest/)
