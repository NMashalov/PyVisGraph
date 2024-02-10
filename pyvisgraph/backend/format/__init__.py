from .processor import GraphProcessor
from fastapi import APIRouter

router = APIRouter(
    prefix="/format"
)

@router.post("/export?{format}")
def export(format:str):