from pyvisgraph.settings.configs import Preset, ConfigsManager
from pyvisgraph.back.mart import OperatorMart, operator_mart
from pyvisgraph.back.graph import GraphManager, graph_manager
from pyvisgraph.api import server
from pyvisgraph.settings.configs import configs_manager
from fastapi import FastAPI
import typing as tp 
import abc

class Meta(type):
    def __init__(cls, name, bases, namespace):

class AbstractSettings:
    pass

class AbstractManager:
    @abc.abstractmethod
    def update_settings(self, cfg: AbstractSettings):
        pass


class PyVisGraphManager:
    def __init__(self,op_mart: OperatorMart, config_manager:  ConfigsManager, graph_manager: GraphManager,server: FastAPI):
        self.op_mart = op_mart
        self.graph_manager = graph_manager
        self.config_manager = config_manager
        self.update_configs()
    

    def update_configs(self):
        self.config_manager = ConfigsManager(cfg)

        ConfigsManager()
        return cls(
            OperatorMart(
                cfg_manager.return_OperatorMartCfg()
            ),
            cfg_manager,
            GraphManager(
                cfg_manager
            ),
            server
        )
    
PyVisGraphManager(operator_mart,configs_manager,graph_manager,server)




    

  





