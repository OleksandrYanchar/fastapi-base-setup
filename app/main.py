import uvicorn
from api.v1.routers import router as v1_router
from configs.db import REDIS_URL
from configs.general import MEDIA_DIR
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

app = FastAPI(
    title="FastAPI Starter Project",
    description="FastAPI Starter Project",
    version="1.0",
    docs_url="/api/docs/",
    redoc_url="/api/redoc/",
    openapi_url="/api/openapi.json",
    default_response_class=UJSONResponse,
)


app.include_router(v1_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/media", StaticFiles(directory=MEDIA_DIR))


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
