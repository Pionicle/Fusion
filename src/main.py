"""
Основной модуль приложения FastAPI.
"""

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
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


# Обработка ошибок соединения с базой данных
@app.exception_handler(ConnectionRefusedError)
async def error_connection_refused_error(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "В соединении с базой данных отказано."},
    )


# Запуск приложения
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
