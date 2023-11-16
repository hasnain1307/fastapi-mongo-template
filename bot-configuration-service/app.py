from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware

from api.users.routes import router as users_router
from api.bots.routes import router as bots_router
from api.tenants.routes import router as tenants_router
from logger import logger

app = FastAPI(
    title="ISSM XIVA BOT",
    description="""Bot configuration API, with auto docs for the API and everything.""",
)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} - status {response.status_code}")
    return response


app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(bots_router, prefix="/api/v1/bots", tags=["bots"])
app.include_router(tenants_router, prefix="/api/v1/tenants", tags=["tenants"])

# TODO: Setup global timestamp for all output models (schemas-pydantic)


@app.get("/")
async def read_root():
    logger.info("Root endpoint hit")
    return status.HTTP_200_OK
