from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home_view():
    return {"message": "I'm from home page"}

@app.get("/about")
async def about_view():
    return {"message": "I'm from about page"}
