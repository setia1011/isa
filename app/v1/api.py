from fastapi import APIRouter
from app.v1.routers import analysis, home, crawler, analysis, install

router_v1 = APIRouter()
router_v1.include_router(home.router, prefix="", tags=["home"])
router_v1.include_router(install.router, prefix="/v1", tags=["install"])
router_v1.include_router(crawler.router, prefix="/v1", tags=["crawler"])
router_v1.include_router(analysis.router, prefix="/v1", tags=["analysis"])