from fastapi import FastAPI, Request, UploadFile, APIRouter, Depends 
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from .configs import configs_router

from pathlib import Path
import json
from contextlib import asynccontextmanager
from pydantic import ValidationError
from .manager import PyVisGraphManager

PATH = Path(__file__).parent.parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    manager = ()
    yield
        # Clean operatorMart
    del manager

server = FastAPI(lifespan=lifespan)
main_router = APIRouter(prefix=f"v1")
main_router.include_router()


@server.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=418, content=exc.json())


@server.get("/operators")
def operators(request: Request, db: PyVisGraphManager = Depends(get_db)):
    return request.app.state.local_nodes


@server.post("/graphs")
async def receive_graph(graph: Request):
    body: dict = json.loads(await graph.body())["body"]
    g = Dag(**body)
    print(g)
    yaml_output = format_dag_to_groups(g)
    print(yaml_output)
    validate_graph(g.graph)
    return yaml_output


server.mount("", StaticFiles(directory=PATH / "web", html=True), name="web")
