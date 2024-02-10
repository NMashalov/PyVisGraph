from fastapi import FastAPI, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi import APIRouter

from pathlib import Path
import json
from contextlib import asynccontextmanager
from pydantic import ValidationError

from .mart import OperatorMart

PATH = Path(__file__).parent.parent

@asynccontextmanager
async def lifespan(app: FastAPI):
    oper = OperatorMart()
    yield
    # Clean operatorMart
    del oper


server = FastAPI(lifespan=lifespan)














@router.get("")
async

