import abc
from pyvisgraph.back.graph import G

class AbstractClassProcessor:
    @abc.abstractmethod
    def return_graph_state():
        raise NotImplementedError()
