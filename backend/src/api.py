from datetime import datetime
from server import app
from pydantic import BaseModel
from .dal import ListSummary, ToDoList
from fastapi import status

@app.get("/api/lists")
async def get_all_lists() -> list[ListSummary]:
    return [list_summary async for list_summary in app.todo_list_dal.list_todo_lists()]


class NewList(BaseModel):
    name: str

class NewListResponse(BaseModel):
    id: str
    name: str

@app.post("/api/lists", status_code=status.HTTP_201_CREATED)
async def create_todo_list(new_list: NewList) -> NewListResponse:
    list_id = await app.state.todo_list_dal.create_todo_list(new_list.name)
    return NewListResponse(id=list_id, name=new_list.name)


@app.get("/api/lists/{list_id}")
async def get_list(list_id: str) -> ToDoList:
    """Get a single list by ID"""
    return await app.state.todo_list_dal.get_todo_list(list_id)

@app.delete("/api/lists/{list_id}")
async def delete_list(list_id: str) -> None:
    """Delete a list by ID"""
    return await app.state.todo_list_dal.delete_todo_list(list_id)
    

class NewItem(BaseModel):
    label: str

class NewItemResponse(BaseModel):
    id: str
    label: str

@app.post("/api/lists/{list_id}/items/", status_code=status.HTTP_201_CREATED)
async def create_item(list_id: str, new_item: NewItem) -> ToDoList:
    return await app.state.todo_list_dal.create_todo_list_item(list_id, new_item.label)
    
@app.delete("/api/lists/{list_id}/items/{item_id}")
async def delete_item(list_id: str, item_id: str) -> ToDoList:
    return await app.state.todo_list_dal.delete_todo_list_item(list_id, item_id)


class TodoItemUpdate(BaseModel):
    item_id: str
    checked: bool

@app.patch("/api/lists/{list_id}/checked_state")
async def update_item(list_id: str, update: TodoItemUpdate) -> ToDoList:
    return await app.state.todo_list_dal.update_todo_list_item(list_id, update.item_id, update.checked)


class DummyResponse(BaseModel):
    id: str
    when: datetime

@app.get("/api/dummy")
async def dummy() -> DummyResponse:
    return DummyResponse(id="dummy", when=datetime.now())
