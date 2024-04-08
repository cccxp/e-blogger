from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import account

app = FastAPI()

api = APIRouter(prefix='/api/v1')
api.include_router(account.router)

allow_origins = [
    "http://localhost:8080",  # frontend development server address
    "http://127.0.0.1:8080",
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
