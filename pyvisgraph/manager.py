from pyvisgraph.configs import Preset, ConfigsManager
from pyvisgraph.api.mart import OperatorMart
from pyvisgraph.api.graph import GraphManager
from pyvisgraph.backend import server
import uvicorn
from fastapi import FastAPI


class PyVisGraphManager:
    def __init__(self,op_mart: OperatorMart, cfg_manager:  ConfigsManager, graph_manager: GraphManager,server: FastAPI):
        self.op_mart = op_mart
        self.graph_manager = graph_manager
        self.config_manager = cfg_manager
    
    @classmethod
    def from_configs(cls,cfg:Preset):
        cfg_manager = ConfigsManager(cfg)
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

        
    def start(self):
        uvicorn.run(self.server)



    

  





