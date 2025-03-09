from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as router_hotels
# from src.config import settings
# print(f"{settings.DB_URL=}")
from src.database import *

app = FastAPI()

app.include_router(router_hotels)
# Варианты запуска:
# fastapi dev main.py
# uvicorn main:app --reload
# python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
