from ...graph.processor import GraphProcessor
from fastapi import APIRouter
from .litegraph import LiteGraphOutput
from contextlib import asynccontextmanager
import typing as tp


@asynccontextmanager
def lifespan():
    processor = GraphProcessor()
    yield
    del processor


import_router = APIRouter(prefix="/import", lifespan=lifespan)


export_router = APIRouter(prefix="/export", lifespan=lifespan)


@import_router.post("/export")
def export(
    format: tp.Literal["linear", "grouped"],
):
    return
