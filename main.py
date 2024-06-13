from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import account, blog, comments
from contextlib import asynccontextmanager
from database import async_engine
from database_models.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    async with async_engine.begin() as engine:
        await engine.run_sync(Base.metadata.create_all)
    yield
    # clean up


app = FastAPI(
    title='E-Blogger',
    description='A simple blogging platform built with FastAPI.',
    version='1.0.1',
    lifespan=lifespan
)

api = APIRouter(prefix='/api/v1')
api.include_router(account.router)
api.include_router(blog.router)
api.include_router(comments.router)

allow_origins = [
    "*",
    # "http://localhost:8080",  # frontend development server address
    # "http://127.0.0.1:8080",
]

app.include_router(api)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", description="used to verify server started successfully.")
def demo():
    return {"Hello": "World"}
