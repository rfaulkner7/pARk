from fastapi import APIRouter

from api.paths.routes import router as path_router

api_router = APIRouter()

api_router.include_router(router=path_router, prefix='/path')
