from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from app.v1.schemas import simple as simple_schema

router = APIRouter()

@router.get("/", response_model=simple_schema.Simple)
async def home():
    return {"detail": "Welcome to Intelligence Socio Analysis (ISA)"}