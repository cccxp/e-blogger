from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from routers import account


app = FastAPI()

api = APIRouter(prefix='/api/v1')
api.include_router(account.router)

app.include_router(api)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", description="used to verify server started successfully.")
def demo():
    return {"Hello": "World"}
