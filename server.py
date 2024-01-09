from fastapi import FastAPI,Request, UploadFile
from fastapi.staticfiles import StaticFiles
import uvicorn 
from pydanticGraph import (
    load_nodes_from_local,
    NODES,
    load_nodes_from_file
)
from pathlib import Path
import json 

PATH = Path(__file__).parent

app = FastAPI()

@app.post('/parse_nodes')
def parse_nodes(file :UploadFile):
    load_nodes_from_file(file)

@app.get('/nodes')
def send_nodes():
    return NODES

@app.post('/graphs')
async def recieve_graph(graph: Request):
    b = await graph.body()
    print(json.loads(b))
    

app.mount("", StaticFiles(directory="web", html=True), name="web")

if __name__ == "__main__":
    load_nodes_from_local(PATH / 'test' / 'nodes.py')
    uvicorn.run(app)