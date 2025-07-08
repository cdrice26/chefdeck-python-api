from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class RootResponse(BaseModel):
    message: str


@router.get("/")
async def root() -> RootResponse:
    return RootResponse(message="You have reached the Cooky Python API.")
