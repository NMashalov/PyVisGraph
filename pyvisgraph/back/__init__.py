from fastapi import FastAPI, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
from pyvisgraph import (
    format_dag_to_groups,
    load_nodes_from_local,
    _NODE_MODELS,
    load_nodes_from_file,
    SETTINGS,
    validate_graph,
    WrongGraphException,
    Dag,
)
from pathlib import Path
import json
from contextlib import asynccontextmanager
from pydantic import ValidationError

PATH = Path(__file__).parent.parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    local_nodes = []
    for path in SETTINGS.paths:
        local_nodes.append(
            load_nodes_from_local(PATH / path.relative_path, path.module_name)
        )
    app.state.local_nodes = local_nodes
    yield
    # Clean up the ML models and release the resources
    del local_nodes


server = FastAPI(lifespan=lifespan)


@server.exception_handler(WrongGraphException)
async def wrong_graph_exception_handler(request: Request, exc: WrongGraphException):
    return JSONResponse(status_code=421, content=str(exc))


@server.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=418, content=exc.json())


@server.get("/dag_fields")
async def send_dag_fields():
    return SETTINGS.dag_settings


@server.post("/parse_nodes")
async def parse_nodes(file: UploadFile):
    return await load_nodes_from_file(file)


@server.get("/local_nodes")
def send_nodes(request: Request):
    return request.app.state.local_nodes


@server.post("/graphs")
async def recieve_graph(graph: Request):
    body: dict = json.loads(await graph.body())["body"]
    g = Dag(**body)
    print(g)
    yaml_output = format_dag_to_groups(g)
    print(yaml_output)
    validate_graph(g.graph)
    return yaml_output


server.mount("", StaticFiles(directory=PATH / "web", html=True), name="web")

  
