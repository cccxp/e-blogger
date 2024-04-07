from fastapi import FastAPI
from routers import account

app = FastAPI()
app.include_router(account.router)

@app.get("/", description="used to verify server started successfully.")
def demo():
    return {"Hello": "World"}
