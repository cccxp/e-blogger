from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def demo():
    return {"Hello": "World"}
