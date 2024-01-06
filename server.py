from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn 
from pydanticGraph import load_custom_node, NODES

app = FastAPI()


@app.get('/nodes')
def send_nodes():
    return NODES


app.mount("", StaticFiles(directory="web", html=True), name="web")

if __name__ == "__main__":
    load_custom_node('./test/hello.py')
    uvicorn.run(app)