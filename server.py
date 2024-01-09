from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn 
from pydanticGraph import load_custom_node, NODES
from pathlib import Path

PATH = Path(__file__).parent

app = FastAPI()


@app.get('/nodes')
def send_nodes():
    return NODES


app.mount("", StaticFiles(directory="web", html=True), name="web")

if __name__ == "__main__":
    load_custom_node(PATH / 'test' / 'nodes.py')
    uvicorn.run(app)