from fastapi import Depends, FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.routers import nutritions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)


app.include_router(nutritions.router)


@app.get("/")
async def root():
    return {"message": "Hello Nutrition search Applications!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)



