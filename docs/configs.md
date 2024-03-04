Dependency in each module comes from main class object, 
who stores module configs as class variable.

For example [mart.py](/pyvisgraph/mart/mart.py)

```python
@dataclass
class OperatorMartCfg:
    file_processor_cfg: FileOperatorProcessorCfg
    import_paths: list[Path]

class OperatorMart:
    """
    Manages collection of
    operators and it's interaction with
    """

    cfg = OperatorMartCfg()

    def __init__(
        self,
        cfg: OperatorMartCfg
    ):
        # Class configs are updated on __init__ operation
```

This allows to escape [properties drilling](https://www.geeksforgeeks.org/what-is-prop-drilling-and-how-to-avoid-it/) in nested dataclassess. 

