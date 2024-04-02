import uvicorn
from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from api.v1.routers import router as v1_router
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


from configs.general import ROOT, setup_logger

router = APIRouter(
    prefix="/api",
    tags=["api"],
)

router.include_router(v1_router)


app = FastAPI(
    title="FastAPI Starter Project",
    description="FastAPI Starter Project",
    version="1.0",
    docs_url="/api/docs/",
    redoc_url="/api/redoc/",
    openapi_url="/api/openapi.json",
    default_response_class=UJSONResponse,
)


app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    app.mount("/static", StaticFiles(directory=ROOT))
except Exception:
    ROOT_PATH = f"../{ROOT}"
    app.mount("/static", StaticFiles(directory=f"{ROOT}"))


setup_logger(ROOT)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
