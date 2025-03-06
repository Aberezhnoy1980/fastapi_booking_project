import asyncio
import time

# Синхронная функция
def get_data_from_database(query: str):
    print(f"Получен запрос: {query}")
    if query == "Сочи":
        time.sleep(4)
    elif query == "Дубай":
        time.sleep(2)
    print("Данные получены: {query}")
    
    
# Асинхронная функция
async def get_data_from_database_async(query: str):
    print(f"Получен запрос: {query}")
    if query == "Сочи":
        await asyncio.sleep(4)
    elif query == "Дубай":
        await asyncio.sleep(2)
    print(f"Данные получены: {query}")
    return "Results"


# Пример асинхроннго вызова с использованием asyncio.gather
async def main():
    tasks = [
        get_data_from_database_async("Сочи"),
        get_data_from_database_async("Дубай")
    ]
    results = await asyncio.gather(*tasks)
    print("Все данные получены:", results)
    

# Запуск программы
asyncio.run(main())

