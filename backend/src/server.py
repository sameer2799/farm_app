from contextlib import asynccontextmanager
from datetime import datetime
import os
import sys

from bson import ObjectId
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import uvicorn

from dal import ListSummary, ToDoListDal, ToDoList

COLLECTION_NAME = "todo_lists"
MONGODB_URI = os.environ["MONGODB_URI"]
DEBUG = os.environ.get("DEBUG", "").strip().lower() in {"true", "1", "yes", "on"}



@asynccontextmanager
async def lifespan(app: FastAPI):
        
    client=AsyncIOMotorClient(MONGODB_URI)
    database = client.get_default_database()

    pong = await database.command("ping")
    if int(pong["ok"]) != 1:
        raise Exception("Failed to connect to MongoDB")
    

    todo_lists = database.get_collection(COLLECTION_NAME)
    app.todo_list_dal = ToDoListDal(todo_lists)

    yield

    client.close()

app = FastAPI(lifespan=lifespan, debug=DEBUG)

origins = [
        "http://localhost:3000"
    ]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/api/lists")
async def get_all_lists() -> list[ListSummary]:
    print("getting all lists...")
    return [list_summary async for list_summary in app.todo_list_dal.list_todo_lists()]


class NewList(BaseModel):
    name: str

class NewListResponse(BaseModel):
    id: str
    name: str

@app.post("/api/lists", status_code=status.HTTP_201_CREATED)
async def create_todo_list(new_list: NewList) -> NewListResponse:
    list_id = await app.todo_list_dal.create_todo_list(new_list.name)
    return NewListResponse(id=list_id, name=new_list.name)


@app.get("/api/lists/{list_id}")
async def get_list(list_id: str) -> ToDoList:
    """Get a single list by ID"""
    return await app.todo_list_dal.get_todo_list(list_id)

@app.delete("/api/lists/{list_id}")
async def delete_list(list_id: str) -> None:
    """Delete a list by ID"""
    return await app.todo_list_dal.delete_todo_list(list_id)
    

class NewItem(BaseModel):
    label: str

class NewItemResponse(BaseModel):
    id: str
    label: str

@app.post("/api/lists/{list_id}/items/", status_code=status.HTTP_201_CREATED)
async def create_item(list_id: str, new_item: NewItem) -> ToDoList:
    return await app.todo_list_dal.create_item(list_id, new_item.label)
    
@app.delete("/api/lists/{list_id}/items/{item_id}")
async def delete_item(list_id: str, item_id: str) -> ToDoList:
    return await app.todo_list_dal.delete_item(list_id, item_id)


class TodoItemUpdate(BaseModel):
    item_id: str
    checked: bool

@app.patch("/api/lists/{list_id}/checked_state")
async def update_item(list_id: str, update: TodoItemUpdate) -> ToDoList:
    return await app.todo_list_dal.set_checked_state(list_id, update.item_id, update.checked)


class DummyResponse(BaseModel):
    id: str
    when: datetime

@app.get("/api/dummy")
async def dummy() -> DummyResponse:
    return DummyResponse(id="dummy", when=datetime.now())


def main(argv=sys.argv[1:]):
    try:
        uvicorn.run("server:app", host="0.0.0.0", port=3001, reload=DEBUG)
    except:
        pass

if __name__ == "__main__":
    main()