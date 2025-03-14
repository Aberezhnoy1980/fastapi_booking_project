import time
import asyncio
import threading

from fastapi import FastAPI
import uvicorn

app = FastAPI(docs_url=None)


@app.get("/sync/{id}")
def sync_func(id: int):
    print(f"sync. Потоков: {threading.active_count()}")
    print(f"sync. Начал {id}: {time.time():.2f}")
    time.sleep(3)
    print(F"sync. Закончил {id}: {time.time():.2f}")


@app.get("/async/{id}")
async def async_func(id: int):
    print(f"async. Потоков: {threading.active_count()}")
    print(f"async. Начал {id}: {time.time():.2f}")
    await asyncio.sleep(2)
    print(F"async. Закончил {id}: {time.time():.2f}")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
    # uvicorn.run("main:app", reload=False, workers=30)
