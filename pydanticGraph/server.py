from fastapi import FastAPI, Request, UploadFile
from fastapi.staticfiles import StaticFiles
import uvicorn
from pydanticGraph import (
    format_to_yaml_groups,
    load_nodes_from_local,
    _NODE_MODELS,
    load_nodes_from_file,
    sequential_groups,
    SETTING
)
from pathlib import Path
import json
from contextlib import asynccontextmanager

PATH = Path(__file__).parent.parent

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    local_nodes = []
    for path in SETTING.paths:
        local_nodes.append(
            load_nodes_from_local(
                PATH / path.relative_path,
                path.module_name
            )
        )
    app.state.local_nodes= local_nodes
    yield
    # Clean up the ML models and release the resources
    del local_nodes


app = FastAPI(lifespan=lifespan)


@app.post("/parse_nodes")
async def parse_nodes(file: UploadFile):
    return await load_nodes_from_file(file)

@app.post("/validate_graph")
async def validate_graph(graph: Request):
    body: dict = json.loads(await graph.body())['body']
    _, g = sequential_groups(body['graph'])
    return validate_graph(g)


@app.get("/local_nodes")
def send_nodes(request: Request):
    print(request.app.state.local_nodes)
    return request.app.state.local_nodes


@app.post("/graphs")
async def recieve_graph(graph: Request):
    body: dict = json.loads(await graph.body())['body']
    print(body)
    groupped_dag, g = sequential_groups(body['graph'])
    yaml_output = format_to_yaml_groups(groupped_dag, g)
    print(yaml_output)
    return yaml_output
    


app.mount("", StaticFiles(directory=PATH / "web", html=True), name="web")


def run():
    uvicorn.run(app)
