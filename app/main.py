from fastapi import Depends, FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.routers.nutritions import router as nutrition_router
app = FastAPI()



app.include_router(nutrition_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello Nutrition search Applications!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)



