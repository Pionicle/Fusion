"""
Основной модуль приложения FastAPI.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.routes_api import router

# Экземпляр приложения
app = FastAPI()


# Подключение путей для api
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"],
    allow_headers=["*"],
)

# Запуск приложения
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
