import json
import os
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/electronics", tags=["electronics"])

DATA_FILE = "electronics.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


class ElectronicsItem(BaseModel):
    name: str
    brand: str
    price: float
    specs: str


# GET — получить все товары с сортировкой и поиском по бренду
@router.get("/")
async def get_electronics(
    sorting: Optional[str] = Query(None, description="Сортировка: asc (А-Я) или desc (Я-А)"),
    brand: Optional[str] = Query(None, description="Поиск по бренду")
):
    items = load_data()

    # Фильтрация по бренду
    if brand:
        items = [i for i in items if i["brand"].lower() == brand.lower()]

    # Сортировка по названию
    if sorting == "asc":
        items = sorted(items, key=lambda x: x["name"].lower())
    elif sorting == "desc":
        items = sorted(items, key=lambda x: x["name"].lower(), reverse=True)

    return {
        "electronics": items,
        "total": len(items)
    }


# GET по бренду — отдельный эндпоинт поиска
@router.get("/search")
async def search_by_brand(
    brand: str = Query(..., description="Название бренда для поиска")
):
    items = load_data()
    result = [i for i in items if i["brand"].lower() == brand.lower()]
    return {
        "electronics": result,
        "total": len(result)
    }


# GET по ID
@router.get("/{item_id}")
async def get_electronics_by_id(item_id: int):
    items = load_data()
    item = next((i for i in items if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return item


# POST — добавить новый товар
@router.post("/")
async def create_electronics(item: ElectronicsItem):
    items = load_data()
    new_id = max((i["id"] for i in items), default=0) + 1
    new_item = {"id": new_id, **item.model_dump()}
    items.append(new_item)
    save_data(items)
    return {"message": "Товар добавлен", "item": new_item}


# PUT — обновить товар
@router.put("/{item_id}")
async def update_electronics(item_id: int, updated: ElectronicsItem):
    items = load_data()
    for i, item in enumerate(items):
        if item["id"] == item_id:
            items[i] = {"id": item_id, **updated.model_dump()}
            save_data(items)
            return {"message": "Товар обновлён", "item": items[i]}
    raise HTTPException(status_code=404, detail="Товар не найден")


# DELETE — удалить товар
@router.delete("/{item_id}")
async def delete_electronics(item_id: int):
    items = load_data()
    new_items = [i for i in items if i["id"] != item_id]
    if len(new_items) == len(items):
        raise HTTPException(status_code=404, detail="Товар не найден")
    save_data(new_items)
    return {"message": f"Товар с id={item_id} удалён"}