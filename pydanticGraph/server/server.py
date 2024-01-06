from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
from fastapi.responses import JSONResponse
from typing import Union


class Server:
    def __init__(self, loop):
        self.loop = loop
        app = FastAPI()
        self.app = app

        @app.get("/")
        def read_root():
            return {"Hello": "World"}

        @app.get("/items/{item_id}")
        def read_item(item_id: int, q: Union[str, None] = None):
            return {"item_id": item_id, "q": q}

    async def start(
        self,
        address: str = "0.0.0.0",
        port: int = 8080,
        verbose=True,
        call_on_start=None,
    ):
        uvicorn.run(self.app, host=address, port=8080, loop=self.loop)

        if address == "":
            address = "0.0.0.0"
        if verbose:
            print("Starting server\n")
            print("To see the GUI go to: http://{}:{}".format(address, port))
        if call_on_start is not None:
            call_on_start(address, port)
