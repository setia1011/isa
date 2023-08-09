from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.v1 import api

def get_application():
    _app = FastAPI(
        debug=True,
        title=settings.PROJECT_NAME,
        version="v1",
        docs_url='/doc-api',
        redoc_url='/redoc-api',
        description="Intelligence Socio Analysis (ISA) is a web based application for analyzing the data from social sources, such as Twitter, Facebook, and LinkedIn.",
        terms_of_service="https://isa.techack.id/terms/",
        contact={
            "name": "Setiadi",
            "url": "https://isa.techack.id/contact/",
            "email": "setiadi@techack.id",
        },
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app

app = get_application()
app.include_router(api.router_v1)
