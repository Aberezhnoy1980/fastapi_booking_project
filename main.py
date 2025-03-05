from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"}
]


@app.get("/hotels")
def get_hotel(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


# body, request body
@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    # for hotel in hotels:
    #     if hotel["id"] == hotel_id:
    #         hotels.remove(hotel)
    # hotels.remove({hotel for hotel in hotels if hotel["id"] == hotel_id}.pop())
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


# Варианты запуска:
# fastapi dev main.py
# uvicorn main:app --reload
# python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
