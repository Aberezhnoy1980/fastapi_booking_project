from fastapi import FastAPI
import uvicorn

from hotels import router as router_hotels

app = FastAPI()

app.include_router(router_hotels)
# Варианты запуска:
# fastapi dev main.py
# uvicorn main:app --reload
# python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
