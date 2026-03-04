import logging

import uvicorn
from fastapi import FastAPI

from src.controllers.electronics import router as electronics_router

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Electronics API",
    description="API для магазина электроники",
    version="1.0.0",
)

app.include_router(electronics_router)

@app.get("/")
async def root():
    return {
        "message": "Это API для магазина электроники",
    }

def main():
    logger.info('Started')
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)

if __name__ == "__main__":
    main()
